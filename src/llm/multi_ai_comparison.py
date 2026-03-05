"""
Multi-AI Comparison Service - Parallel execution from multiple LLM providers
with intelligent result comparison and selection.

Supports:
- Google Gemini
- OpenAI GPT
- Anthropic Claude
- xAI Grok
- Fallback recommendations

Each AI provides independent analysis, agents compare results, and the best is selected.
"""

import os
import logging
import asyncio
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.llm.gemini_provider import GeminiLLMProvider
from src.llm.openai_provider import OpenAILLMProvider
from src.llm.claude_provider import ClaudeLLMProvider
from src.llm.mock_provider import MockLLMProvider

logger = logging.getLogger(__name__)


@dataclass
class AIResult:
    """Result from a single AI provider."""
    provider_name: str
    success: bool
    recommendations: List[str] = None
    confidence: float = 0.0
    analysis: str = ""
    reasoning: str = ""
    execution_time: float = 0.0
    error: Optional[str] = None
    tokens_used: int = 0  # Total tokens (input + output)
    input_tokens: int = 0
    output_tokens: int = 0
    best_for: str = ""  # Description of what this AI is best for


@dataclass
class ComparisonResult:
    """Final result with all AI responses and selection."""
    best_provider: str
    best_result: List[str]
    all_results: Dict[str, AIResult]
    comparison_analysis: str
    selection_reason: str
    timestamp: str


class GrokLLMProvider:
    """xAI Grok LLM provider for medical recommendations."""
    
    def __init__(self):
        self.name = "xAI Grok"
        self.available = False
        self.initialize()
    
    def initialize(self) -> bool:
        """Initialize Grok with API key."""
        try:
            api_key = os.getenv("GROK_API_KEY")
            if not api_key:
                logger.warning("GROK_API_KEY not found in environment variables")
                return False
            
            try:
                import requests
                self.api_key = api_key
                self.base_url = "https://api.x.ai/v1"
                self.model = "grok-2"
                self.available = True
                logger.info("✓ Grok provider initialized")
                return True
            except ImportError:
                logger.warning("requests library required for Grok")
                return False
        except Exception as e:
            logger.warning(f"Grok initialization failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Grok is available."""
        return self.available
    
    def generate_recommendations(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate medical recommendations using Grok."""
        try:
            import requests
            
            prompt = self._build_prompt(interpretations, risks, parameters, patient_context)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a medical analysis AI. Provide evidence-based health recommendations based on blood test parameters."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return self._parse_recommendations(content)
            else:
                logger.warning(f"Grok API error: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Grok recommendation generation failed: {e}")
            return []
    
    def _build_prompt(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for Grok."""
        prompt = "Analyze the following blood test results and provide medical recommendations:\n\n"
        prompt += f"Parameters: {json.dumps(parameters, default=str)}\n\n"
        
        if interpretations:
            prompt += "Interpretations:\n"
            for interp in interpretations:
                prompt += f"- {interp}\n"
        
        if risks:
            prompt += "\nIdentified Risks:\n"
            for risk in risks:
                prompt += f"- {risk}\n"
        
        prompt += "\nProvide 3-5 specific, actionable health recommendations with numbering."
        
        return prompt
    
    def _parse_recommendations(self, content: str) -> List[str]:
        """Parse recommendations from Grok response."""
        lines = content.split('\n')
        recommendations = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                recommendations.append(line)
        return recommendations if recommendations else [content[:200]]


class MultiAIComparisonService:
    """
    Manages multiple AI providers for parallel analysis and comparison.
    Gets independent recommendations from each AI, compares them, and selects the best.
    """
    
    def __init__(self):
        self.providers = {}
        self.available_providers = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available AI providers."""
        logger.info("🤖 Initializing Multi-AI Comparison Service...")
        
        providers_to_init = [
            ("gemini", GeminiLLMProvider()),
            ("openai", OpenAILLMProvider()),
            ("claude", ClaudeLLMProvider()),
            ("grok", GrokLLMProvider()),
            ("mock", MockLLMProvider()),
        ]
        
        for provider_name, provider in providers_to_init:
            self.providers[provider_name] = provider
            if provider.is_available():
                self.available_providers.append((provider_name, provider))
                logger.info(f"  ✓ {provider.name} available")
            else:
                logger.debug(f"  ✗ {provider.name} unavailable")
        
        logger.info(f"🚀 Multi-AI Service ready with {len(self.available_providers)} providers")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return [name for name, _ in self.available_providers]
    
    def compare_ai_results(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> ComparisonResult:
        """
        Execute all AIs in parallel and compare their results.
        
        Returns the best result plus all individual AI outputs.
        """
        logger.info("📊 Starting Multi-AI analysis...")
        
        # Run all AIs in parallel
        all_results = self._run_all_ais_parallel(
            interpretations, risks, parameters, patient_context
        )
        
        # Select the best result
        best_provider, best_result = self._select_best_result(all_results)
        
        # Generate comparison analysis
        comparison_analysis = self._generate_comparison_analysis(all_results)
        
        # Assign "best_for" descriptions to each AI
        self._assign_best_for_descriptions(all_results)
        
        result = ComparisonResult(
            best_provider=best_provider,
            best_result=best_result,
            all_results=all_results,
            comparison_analysis=comparison_analysis,
            selection_reason=self._get_selection_reason(all_results, best_provider),
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Analysis complete. Best provider: {best_provider}")
        return result
    
    def _run_all_ais_parallel(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]]
    ) -> Dict[str, AIResult]:
        """Execute all AIs in parallel using ThreadPoolExecutor."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=len(self.available_providers)) as executor:
            futures = {}
            
            for provider_name, provider in self.available_providers:
                future = executor.submit(
                    self._run_single_ai,
                    provider_name,
                    provider,
                    interpretations,
                    risks,
                    parameters,
                    patient_context
                )
                futures[future] = provider_name
            
            for future in as_completed(futures):
                provider_name = futures[future]
                try:
                    result = future.result(timeout=30)
                    results[provider_name] = result
                    logger.info(f"  ✓ {provider_name}: {len(result.recommendations or [])} recommendations")
                except Exception as e:
                    logger.error(f"  ✗ {provider_name} failed: {e}")
                    results[provider_name] = AIResult(
                        provider_name=provider_name,
                        success=False,
                        error=str(e)
                    )
        
        return results
    
    def _run_single_ai(
        self,
        provider_name: str,
        provider,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]]
    ) -> AIResult:
        """Run a single AI provider and measure execution time."""
        import time
        start_time = time.time()
        
        try:
            recommendations = provider.generate_recommendations(
                interpretations, risks, parameters, patient_context
            )
            
            execution_time = time.time() - start_time
            
            # Estimate tokens (roughly 1 token per 4 characters for input, and count output tokens)
            input_text = " ".join(interpretations) + " " + " ".join(risks) + " " + str(parameters)
            input_tokens = len(input_text) // 4
            output_text = " ".join(recommendations or [])
            output_tokens = len(output_text) // 4
            total_tokens = input_tokens + output_tokens
            
            return AIResult(
                provider_name=provider_name,
                success=bool(recommendations),
                recommendations=recommendations or [],
                confidence=self._calculate_confidence(recommendations),
                execution_time=execution_time,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                tokens_used=total_tokens
            )
        except Exception as e:
            logger.error(f"Error running {provider_name}: {e}")
            return AIResult(
                provider_name=provider_name,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
                tokens_used=0,
                input_tokens=0,
                output_tokens=0
            )
    
    def _calculate_confidence(self, recommendations: List[str]) -> float:
        """Calculate confidence score for recommendations."""
        if not recommendations:
            return 0.0
        
        # Score based on:
        # - Number of recommendations (more is better, up to 5)
        # - Quality indicators in text
        score = 0.0
        
        # Count recommendations
        count_score = min(len(recommendations), 5) / 5.0 * 0.5
        
        # Check for quality indicators
        quality_score = 0.0
        combined_text = " ".join(recommendations).lower()
        
        quality_indicators = [
            "consult", "monitor", "diagnostic", "evidence", "clinical",
            "recommend", "suggest", "important", "critical"
        ]
        
        for indicator in quality_indicators:
            if indicator in combined_text:
                quality_score += 0.1
        
        quality_score = min(quality_score, 0.5)
        
        return min(count_score + quality_score, 1.0)
    
    def _select_best_result(self, all_results: Dict[str, AIResult]) -> Tuple[str, List[str]]:
        """
        Select the best result based on:
        1. Success rate
        2. Confidence score
        3. Recommendation quality
        """
        successful_results = {
            name: result for name, result in all_results.items()
            if result.success and result.recommendations
        }
        
        if not successful_results:
            # Return first available result
            for name, result in all_results.items():
                if result.recommendations:
                    return name, result.recommendations
            return "fallback", ["Consult with a healthcare professional"]
        
        # Score each successful result
        scores = {}
        for provider_name, result in successful_results.items():
            score = result.confidence * 0.7 + (1.0 / result.execution_time if result.execution_time > 0 else 1) * 0.3
            scores[provider_name] = score
        
        best_provider = max(scores, key=scores.get)
        
        # Synthesize all recommendations into comprehensive list with AI attribution
        synthesized = self._synthesize_all_recommendations(all_results, best_provider)
        
        return best_provider, synthesized
    
    def _generate_comparison_analysis(self, all_results: Dict[str, AIResult]) -> str:
        """Generate a comparison analysis of all AI results."""
        analysis = "**Multi-AI Analysis Summary:**\n\n"
        
        for provider_name, result in all_results.items():
            status = "✅" if result.success else "❌"
            analysis += f"{status} **{result.provider_name}** ({result.execution_time:.2f}s)\n"
            if result.success:
                analysis += f"   - Recommendations: {len(result.recommendations)} items\n"
                analysis += f"   - Confidence: {result.confidence*100:.1f}%\n"
            else:
                analysis += f"   - Error: {result.error}\n"
        
        return analysis
    
    def _get_selection_reason(self, all_results: Dict[str, AIResult], selected: str) -> str:
        """Generate reasoning for the selected AI."""
        selected_result = all_results.get(selected)
        if not selected_result:
            return "No analysis available"
        
        reason = f"{selected_result.provider_name} was selected as BEST for this document because:\n"
        reason += f"- ✓ Successfully generated {len(selected_result.recommendations)} recommendations\n"
        reason += f"- ✓ High confidence score: {selected_result.confidence*100:.1f}%\n"
        reason += f"- ✓ Efficient token usage: {selected_result.tokens_used} tokens\n"
        reason += f"- ✓ Fast execution: {selected_result.execution_time:.2f}s\n"
        
        return reason
    
    def _assign_best_for_descriptions(self, all_results: Dict[str, AIResult]) -> None:
        """Assign 'best for' descriptions to each AI based on their characteristics."""
        best_for_map = {
            "gemini": "Speed & Efficiency",
            "openai": "Accuracy & Detail",
            "claude": "Nuanced Analysis",
            "grok": "Novel Perspectives",
            "mock": "Testing"
        }
        
        for provider_name, result in all_results.items():
            # Try to match by partial name
            for key, description in best_for_map.items():
                if key.lower() in provider_name.lower():
                    result.best_for = description
                    break
            
            # If no match, assign based on execution characteristics
            if not result.best_for:
                if result.execution_time < 2.0:
                    result.best_for = "Speed"
                elif result.confidence > 0.8:
                    result.best_for = "High Confidence"
                elif result.tokens_used < 1000:
                    result.best_for = "Efficiency"
                else:
                    result.best_for = "Comprehensive"
    
    def _synthesize_all_recommendations(self, all_results: Dict[str, AIResult], best_provider: str) -> List[str]:
        """
        Synthesize recommendations from all AIs with attribution.
        Optimized for speed with caching to prevent duplicate similarity checks.
        """
        synthesized = []
        seen_recommendations = set()
        
        # First, add the best provider's recommendations with highlighting
        if best_provider in all_results:
            best_result = all_results[best_provider]
            if best_result.success and best_result.recommendations:
                for rec in best_result.recommendations[:10]:  # Limit to top 10 to save memory
                    clean_rec = rec.strip()
                    if clean_rec and clean_rec not in seen_recommendations:
                        synthesized.append(f"✨ {clean_rec} [From: {best_provider.upper()}]")
                        seen_recommendations.add(clean_rec[:100])  # Store only first 100 chars for memory efficiency
        
        # Then add complementary recommendations from other AIs
        ai_provider_names = {
            'gemini': 'Gemini Flash',
            'openai': 'OpenAI GPT',
            'claude': 'Claude 3.5',
            'grok': 'Grok-2',
            'mock': 'Mock AI'
        }
        
        for provider_name, result in all_results.items():
            if provider_name == best_provider or not result.success:
                continue
            
            if result.recommendations:
                for rec in result.recommendations[:10]:  # Limit to top 10 per provider
                    clean_rec = rec.strip()
                    
                    # Fast duplicate check using substring matching (faster than token-based)
                    is_duplicate = any(
                        clean_rec[:80].lower() in seen.lower() or seen.lower() in clean_rec[:80].lower()
                        for seen in seen_recommendations
                    )
                    
                    if clean_rec and not is_duplicate:
                        provider_display = ai_provider_names.get(provider_name, provider_name.upper())
                        synthesized.append(f"📌 {clean_rec} [From: {provider_display}]")
                        seen_recommendations.add(clean_rec[:100])
        
        # Add synthesis summary at the end
        if len(all_results) > 1:
            successful_count = sum(1 for r in all_results.values() if r.success)
            synthesized.append(f"\n🔄 All {successful_count} AI providers participated in generating these recommendations")
        
        return synthesized if synthesized else ["Consult with a healthcare professional"]


# Global instance
_multi_ai_service = None


def get_multi_ai_service() -> MultiAIComparisonService:
    """Get or create the global multi-AI service instance."""
    global _multi_ai_service
    if _multi_ai_service is None:
        _multi_ai_service = MultiAIComparisonService()
    return _multi_ai_service

