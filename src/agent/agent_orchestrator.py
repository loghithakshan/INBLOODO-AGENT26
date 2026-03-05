"""
Multi-Agent Orchestrator for Health Diagnostics.

Coordinates multiple AI agents to analyze blood reports:
- Parameter Extraction Agent
- Data Validation Agent
- Interpretation Agent (Model 1)
- Risk Analysis Agent (Model 2)
- Prediction Agent
- LLM Recommendation Agent
- Report Generation Agent
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from src.data_cleaning.data_cleaner import clean_and_structure_data
from src.models.model_1_parameter_interpretation import interpret_parameters
from src.models.model_2_pattern_analysis import analyze_risks
from src.analysis.predictor import predict_risk
from src.llm.multi_llm_service import get_multi_llm_service
from src.llm.multi_ai_comparison import get_multi_ai_service, ComparisonResult
from src.recommendation.recommendation_generator import generate_recommendations, generate_prescriptions, generate_medicines
from src.synthesis.findings_synthesizer import synthesize_findings

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Result from an individual agent."""
    agent_name: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class AnalysisReport:
    """Final analysis report from the multi-agent system."""
    status: str
    extracted_parameters: Dict[str, Any]
    interpretations: List[str]
    risks: List[str]
    ai_prediction: Dict[str, Any]
    recommendations: List[str]
    medicines: List[str]
    prescriptions: List[str]
    synthesis: str
    agent_results: List[AgentResult]
    timestamp: str
    multi_ai_results: Optional[Dict[str, Any]] = None
    best_provider: Optional[str] = None
    selection_reason: Optional[str] = None


class ParameterExtractionAgent:
    """Agent responsible for extracting and cleaning medical parameters."""
    
    def __init__(self):
        self.name = "Parameter Extraction Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(self, raw_params: Dict[str, Any]) -> AgentResult:
        """Extract and clean medical parameters."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info(f"Processing {len(raw_params)} raw parameters")
            cleaned_params = clean_and_structure_data(raw_params)
            
            if not cleaned_params:
                raise ValueError("No valid medical parameters found after cleaning")
            
            execution_time = time.time() - start_time
            self.logger.info(f"Successfully processed {len(cleaned_params)} parameters in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=cleaned_params,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Parameter extraction failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                error=str(e)
            )


class InterpretationAgent:
    """Agent responsible for interpreting blood parameters (Model 1)."""
    
    def __init__(self):
        self.name = "Parameter Interpretation Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(self, cleaned_params: Dict[str, Any]) -> AgentResult:
        """Interpret medical parameters using Model 1."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting parameter interpretation")
            interpretations = interpret_parameters(cleaned_params)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated {len(interpretations)} interpretations in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=interpretations,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Parameter interpretation failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data=[],
                error=str(e)
            )


class RiskAnalysisAgent:
    """Agent responsible for analyzing health risks (Model 2)."""
    
    def __init__(self):
        self.name = "Risk Analysis Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(self, cleaned_params: Dict[str, Any], interpretations: List[str]) -> AgentResult:
        """Analyze risks using Model 2."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting risk analysis")
            risks = analyze_risks(cleaned_params, interpretations)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Identified {len(risks)} risks in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=risks,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Risk analysis failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data=[],
                error=str(e)
            )


class PredictionAgent:
    """Agent responsible for AI-based risk prediction."""
    
    def __init__(self):
        self.name = "AI Prediction Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(self, cleaned_params: Dict[str, Any]) -> AgentResult:
        """Generate AI prediction for health risk."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting AI risk prediction")
            prediction = predict_risk(cleaned_params)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated risk prediction in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=prediction,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"AI prediction failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data={"risk_score": 0.5, "risk_label": "moderate", "confidence": "low"},
                error=str(e)
            )


class LLMRecommendationAgent:
    """Agent responsible for generating LLM-based recommendations using multiple LLM providers."""
    
    def __init__(self):
        self.name = "LLM Recommendation Agent"
        self.logger = logging.getLogger(self.name)
        self.multi_llm_service = get_multi_llm_service()
    
    async def execute(
        self,
        interpretations: List[str],
        risks: List[str],
        cleaned_params: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """Generate recommendations using multiple LLM providers with fallback (Async)."""
        import time
        start_time = time.time()
        
        try:
            # Check availability first (fast, no I/O usually)
            if not self.multi_llm_service.is_any_available():
                self.logger.warning("No LLM providers available, using fallback recommendations")
                return self._fallback_recommendations(interpretations, risks)
            
            available_providers = self.multi_llm_service.get_available_providers()
            self.logger.info(f"Requesting recommendations from available LLMs: {', '.join(available_providers)}")
            
            # Run blocking LLM call in a thread
            recommendations = await asyncio.to_thread(
                self.multi_llm_service.generate_medical_recommendations,
                interpretations=interpretations,
                risks=risks,
                parameters=cleaned_params,
                patient_context=patient_context
            )
            
            execution_time = time.time() - start_time
            
            if recommendations:
                provider_info = self.multi_llm_service.get_provider_info()
                self.logger.info(f"Generated {len(recommendations)} LLM recommendations in {execution_time:.2f}s using {provider_info['primary']}")
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data=recommendations,
                    execution_time=execution_time
                )
            else:
                self.logger.warning("Empty response from all LLMs, using fallback")
                return self._fallback_recommendations(interpretations, risks)
        
        except Exception as e:
            self.logger.error(f"LLM recommendation generation failed: {str(e)}")
            return self._fallback_recommendations(interpretations, risks)
    
    def _fallback_recommendations(self, interpretations: List[str], risks: List[str]) -> AgentResult:
        """Fallback to rule-based recommendations."""
        try:
            recommendations = generate_recommendations(interpretations, risks)
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=recommendations,
                error="LLM unavailable, using fallback recommendations"
            )
        except Exception as e:
            self.logger.error(f"Fallback recommendations failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data=["Consult healthcare provider for personalized advice"],
                error=str(e)
            )


class MultiAIComparisonAgent:
    """Agent that compares results from multiple AI providers and selects the best one."""
    
    def __init__(self):
        self.name = "Multi-AI Comparison Agent"
        self.logger = logging.getLogger(self.name)
        self.multi_ai_service = get_multi_ai_service()
    
    async def execute(
        self,
        interpretations: List[str],
        risks: List[str],
        cleaned_params: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """Compare results from all available AIs and select the best."""
        import time
        start_time = time.time()
        
        try:
            available_providers = self.multi_ai_service.get_available_providers()
            self.logger.info(f"📊 Starting Multi-AI comparison with {len(available_providers)} providers: {available_providers}")
            
            # Run comparison in a thread
            comparison_result = await asyncio.to_thread(
                self.multi_ai_service.compare_ai_results,
                interpretations=interpretations,
                risks=risks,
                parameters=cleaned_params,
                patient_context=patient_context
            )
            
            execution_time = time.time() - start_time
            
            # Log results
            self.logger.info(f"✅ Multi-AI comparison completed in {execution_time:.2f}s")
            self.logger.info(f"🏆 Best provider: {comparison_result.best_provider}")
            self.logger.info(f"📈 Analysis: {comparison_result.comparison_analysis}")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=comparison_result,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Multi-AI comparison failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                error=str(e)
            )




class PrescriptionAgent:
    """Agent responsible for generating prescriptions."""
    
    def __init__(self):
        self.name = "Prescription Generation Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(
        self,
        interpretations: List[str],
        risks: List[str],
        cleaned_params: Dict[str, Any]
    ) -> AgentResult:
        """Generate prescriptions based on analysis."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting prescription generation")
            prescriptions = generate_prescriptions(interpretations, risks, cleaned_params)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated {len(prescriptions)} prescriptions in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=prescriptions,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Prescription generation failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data=[],
                error=str(e)
            )


class MedicinesAgent:
    """Agent responsible for generating medicine and supplement suggestions."""
    
    def __init__(self):
        self.name = "Medicines & Supplements Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(
        self,
        interpretations: List[str],
        risks: List[str],
        cleaned_params: Dict[str, Any]
    ) -> AgentResult:
        """Generate medicines and supplement suggestions based on analysis."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting medicines and supplements generation")
            medicines = generate_medicines(interpretations, risks, cleaned_params)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated {len(medicines)} medicine suggestions in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=medicines,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Medicines generation failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data=[],
                error=str(e)
            )


class SynthesisAgent:
    """Agent responsible for synthesizing all findings into a coherent summary."""
    
    def __init__(self):
        self.name = "Findings Synthesis Agent"
        self.logger = logging.getLogger(self.name)
    
    def execute(
        self,
        parameters: Dict[str, Any],
        interpretations: List[str],
        risks: List[str],
        recommendations: List[str]
    ) -> AgentResult:
        """Synthesize all findings into a summary."""
        import time
        start_time = time.time()
        
        try:
            self.logger.info("Starting findings synthesis")
            synthesis = synthesize_findings(parameters, interpretations, risks, recommendations)
            
            execution_time = time.time() - start_time
            self.logger.info(f"Generated synthesis in {execution_time:.2f}s")
            
            return AgentResult(
                agent_name=self.name,
                success=True,
                data=synthesis,
                execution_time=execution_time
            )
        except Exception as e:
            self.logger.error(f"Findings synthesis failed: {str(e)}")
            return AgentResult(
                agent_name=self.name,
                success=False,
                data="",
                error=str(e)
            )


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents to perform comprehensive health analysis.
    
    Workflow:
    1. Parameter Extraction Agent -> clean and normalize data
    2. Interpretation Agent -> interpret parameters (Model 1)
    3. Risk Analysis Agent -> analyze risks (Model 2)
    4. Prediction Agent -> AI risk prediction
    5. LLM Recommendation Agent -> generate recommendations via Gemini API
    6. Prescription Agent -> generate prescriptions
    7. Synthesis Agent -> synthesize all findings
    """
    
    def __init__(self):
        self.logger = logging.getLogger("MultiAgentOrchestrator")
        self.extraction_agent = ParameterExtractionAgent()
        self.interpretation_agent = InterpretationAgent()
        self.risk_analysis_agent = RiskAnalysisAgent()
        self.prediction_agent = PredictionAgent()
        self.llm_recommendation_agent = LLMRecommendationAgent()
        self.multi_ai_comparison_agent = MultiAIComparisonAgent()
        self.prescription_agent = PrescriptionAgent()
        self.medicines_agent = MedicinesAgent()
        self.synthesis_agent = SynthesisAgent()
        self.agent_results: List[AgentResult] = []
    
    async def execute(
        self,
        raw_params: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> AnalysisReport:
        """
        Execute the multi-agent workflow to analyze health data.
        Optimized with PARALLEL execution for speed.
        
        Args:
            raw_params: Raw medical parameters from input
            patient_context: Optional patient context (age, gender, etc.)
        
        Returns:
            AnalysisReport with results from all agents
        """
        import time
        overall_start = time.time()
        self.agent_results = []
        
        self.logger.info("Starting multi-agent health analysis workflow (PARALLEL MODE)")
        self.logger.info(f"Input parameters: {len(raw_params)}")
        
        # Stage 1: Extract and clean parameters (fast)
        extraction_result = self.extraction_agent.execute(raw_params)
        self.agent_results.append(extraction_result)
        
        if not extraction_result.success:
            self.logger.error("Parameter extraction failed, cannot continue")
            return self._create_failed_report(extraction_result)
        
        cleaned_params = extraction_result.data or {}
        
        # PARALLEL STAGES 2-4: These all depend only on cleaned_params, run in parallel
        stage_start = time.time()
        interpretation_task = asyncio.create_task(
            asyncio.to_thread(self.interpretation_agent.execute, cleaned_params)
        )
        risk_task = asyncio.create_task(
            asyncio.to_thread(
                self.risk_analysis_agent.execute,
                cleaned_params,
                []  # Will get interpretations from parallel execution
            )
        )
        prediction_task = asyncio.create_task(
            asyncio.to_thread(self.prediction_agent.execute, cleaned_params)
        )
        
        # Wait for all parallel tasks with timeout
        try:
            interpretation_result, risk_result, prediction_result = await asyncio.wait_for(
                asyncio.gather(interpretation_task, risk_task, prediction_task),
                timeout=15.0
            )
        except asyncio.TimeoutError:
            self.logger.warning("Parallel agent execution timed out, using fallbacks")
            interpretation_result = AgentResult(self.interpretation_agent.name, False, [])
            risk_result = AgentResult(self.risk_analysis_agent.name, False, [])
            prediction_result = AgentResult(self.prediction_agent.name, False, {})
        
        self.agent_results.extend([interpretation_result, risk_result, prediction_result])
        
        parallel_time = time.time() - stage_start
        self.logger.info(f"Parallel agent execution completed in {parallel_time:.2f}s")
        
        interpretations = interpretation_result.data or []
        risks = risk_result.data or []
        ai_prediction = prediction_result.data or {}
        
        # Re-analyze risks with interpretations if they weren't available
        if not risks and interpretations:
            risk_result = self.risk_analysis_agent.execute(cleaned_params, interpretations)
            self.agent_results.append(risk_result)
            risks = risk_result.data or []
        
        # Stage 5: Generate recommendations via LLM (with timeout to prevent hanging)
        try:
            llm_result = await asyncio.wait_for(
                self.llm_recommendation_agent.execute(
                    interpretations,
                    risks,
                    cleaned_params,
                    patient_context
                ),
                timeout=10.0  # 10s for faster fallback
            )
            self.agent_results.append(llm_result)
            recommendations = llm_result.data or []
        except asyncio.TimeoutError:
            self.logger.warning("LLM timeout (10s), using fast fallback")
            recommendations = self._generate_quick_fallback_recommendations(cleaned_params, interpretations, risks)
        
        # Stage 6: Run prescriptions, medicines, and synthesis in PARALLEL (they don't depend on each other)
        # Each task has individual timeout, overall has longer timeout
        prescription_result = None
        medicines_result = None
        synthesis_result = None
        
        try:
            async def run_prescription_with_timeout():
                try:
                    return await asyncio.wait_for(
                        asyncio.to_thread(
                            self.prescription_agent.execute,
                            interpretations,
                            risks,
                            cleaned_params
                        ),
                        timeout=8.0
                    )
                except asyncio.TimeoutError:
                    self.logger.warning("Prescription agent timed out, using fallback")
                    from src.recommendation.recommendation_generator import generate_prescriptions
                    fallback_prescriptions = generate_prescriptions(interpretations, risks, cleaned_params)
                    return AgentResult(self.prescription_agent.name, False, fallback_prescriptions, "Timeout - fallback")
                except Exception as e:
                    self.logger.error(f"Prescription agent failed: {str(e)}")
                    from src.recommendation.recommendation_generator import generate_prescriptions
                    fallback_prescriptions = generate_prescriptions(interpretations, risks, cleaned_params)
                    return AgentResult(self.prescription_agent.name, False, fallback_prescriptions, str(e))
            
            async def run_medicines_with_timeout():
                try:
                    return await asyncio.wait_for(
                        asyncio.to_thread(
                            self.medicines_agent.execute,
                            interpretations,
                            risks,
                            cleaned_params
                        ),
                        timeout=8.0
                    )
                except asyncio.TimeoutError:
                    self.logger.warning("Medicines agent timed out, using fallback")
                    from src.recommendation.recommendation_generator import generate_medicines
                    fallback_medicines = generate_medicines(interpretations, risks, cleaned_params)
                    return AgentResult("Medicines Agent", False, fallback_medicines, "Timeout - fallback")
                except Exception as e:
                    self.logger.error(f"Medicines agent failed: {str(e)}")
                    from src.recommendation.recommendation_generator import generate_medicines
                    fallback_medicines = generate_medicines(interpretations, risks, cleaned_params)
                    return AgentResult("Medicines Agent", False, fallback_medicines, str(e))
            
            async def run_synthesis_with_timeout():
                try:
                    return await asyncio.wait_for(
                        asyncio.to_thread(
                            self.synthesis_agent.execute,
                            cleaned_params,
                            interpretations,
                            risks,
                            recommendations
                        ),
                        timeout=8.0
                    )
                except asyncio.TimeoutError:
                    self.logger.warning("Synthesis agent timed out, using fallback")
                    fallback_synthesis = f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks."
                    return AgentResult(self.synthesis_agent.name, False, fallback_synthesis, "Timeout - fallback")
                except Exception as e:
                    self.logger.error(f"Synthesis agent failed: {str(e)}")
                    fallback_synthesis = f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks."
                    return AgentResult(self.synthesis_agent.name, False, fallback_synthesis, str(e))
            
            # Run all three in parallel with 20s overall timeout (individual 8s each)
            prescription_result, medicines_result, synthesis_result = await asyncio.wait_for(
                asyncio.gather(
                    run_prescription_with_timeout(),
                    run_medicines_with_timeout(),
                    run_synthesis_with_timeout()
                ),
                timeout=20.0  # Increased from 10s to 20s for safety margin
            )
            
        except asyncio.TimeoutError:
            self.logger.error("Parallel processing exceeded 20s timeout (CRITICAL)")
            from src.recommendation.recommendation_generator import generate_prescriptions, generate_medicines
            # All tasks timed out - use absolute fallbacks
            prescription_result = prescription_result or AgentResult(
                self.prescription_agent.name, False,
                generate_prescriptions(interpretations, risks, cleaned_params),
                "Critical timeout - fallback"
            )
            medicines_result = medicines_result or AgentResult(
                "Medicines Agent", False,
                generate_medicines(interpretations, risks, cleaned_params),
                "Critical timeout - fallback"
            )
            synthesis_result = synthesis_result or AgentResult(
                self.synthesis_agent.name, False,
                f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks.",
                "Critical timeout - fallback"
            )
        except Exception as e:
            self.logger.error(f"Parallel processing failed: {str(e)}")
            from src.recommendation.recommendation_generator import generate_prescriptions, generate_medicines
            # Unexpected error - use absolute fallbacks
            prescription_result = prescription_result or AgentResult(
                self.prescription_agent.name, False,
                generate_prescriptions(interpretations, risks, cleaned_params),
                "Error - fallback"
            )
            medicines_result = medicines_result or AgentResult(
                "Medicines Agent", False,
                generate_medicines(interpretations, risks, cleaned_params),
                "Error - fallback"
            )
            synthesis_result = synthesis_result or AgentResult(
                self.synthesis_agent.name, False,
                f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks.",
                "Error - fallback"
            )
        
        self.agent_results.extend([prescription_result, medicines_result, synthesis_result])
        
        prescriptions = prescription_result.data or []
        medicines = medicines_result.data or []
        synthesis = synthesis_result.data or ""
        
        overall_time = time.time() - overall_start
        
        # Build final report with sorted, formatted results
        report = AnalysisReport(
            status="success",
            extracted_parameters=self._format_parameters_with_descriptions(cleaned_params),
            interpretations=self._sort_interpretations(interpretations),
            risks=self._sort_risks(risks),
            ai_prediction=ai_prediction,
            recommendations=self._sort_recommendations(recommendations),
            medicines=medicines,
            prescriptions=self._sort_prescriptions(prescriptions),
            synthesis=synthesis,
            agent_results=self.agent_results,
            timestamp=datetime.now().isoformat()
        )
        
        self.logger.info(f"Multi-agent analysis completed in {overall_time:.2f}s (OPTIMIZED)")
        self._log_agent_summary(report)
        
        return report
    
    async def execute_with_multi_ai(
        self,
        raw_params: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> AnalysisReport:
        """
        Execute multi-agent workflow WITH MULTI-AI COMPARISON.
        Compares results from Gemini, OpenAI, Claude, and Grok.
        
        Args:
            raw_params: Raw medical parameters from input
            patient_context: Optional patient context (age, gender, etc.)
        
        Returns:
            AnalysisReport with all AI results and the selected best one
        """
        import time
        overall_start = time.time()
        self.agent_results = []
        
        self.logger.info("🚀 Starting multi-agent health analysis WITH MULTI-AI COMPARISON")
        self.logger.info(f"Input parameters: {len(raw_params)}")
        
        # Stage 1: Extract and clean parameters
        extraction_result = self.extraction_agent.execute(raw_params)
        self.agent_results.append(extraction_result)
        
        if not extraction_result.success:
            self.logger.error("Parameter extraction failed, cannot continue")
            return self._create_failed_report(extraction_result)
        
        cleaned_params = extraction_result.data or {}
        
        # PARALLEL STAGES 2-4: Run in parallel
        stage_start = time.time()
        interpretation_task = asyncio.create_task(
            asyncio.to_thread(self.interpretation_agent.execute, cleaned_params)
        )
        risk_task = asyncio.create_task(
            asyncio.to_thread(
                self.risk_analysis_agent.execute,
                cleaned_params,
                []
            )
        )
        prediction_task = asyncio.create_task(
            asyncio.to_thread(self.prediction_agent.execute, cleaned_params)
        )
        
        try:
            interpretation_result, risk_result, prediction_result = await asyncio.wait_for(
                asyncio.gather(interpretation_task, risk_task, prediction_task),
                timeout=15.0
            )
        except asyncio.TimeoutError:
            self.logger.warning("Parallel agent execution timed out, using fallbacks")
            interpretation_result = AgentResult(self.interpretation_agent.name, False, [])
            risk_result = AgentResult(self.risk_analysis_agent.name, False, [])
            prediction_result = AgentResult(self.prediction_agent.name, False, {})
        
        self.agent_results.extend([interpretation_result, risk_result, prediction_result])
        
        parallel_time = time.time() - stage_start
        self.logger.info(f"Parallel agent execution completed in {parallel_time:.2f}s")
        
        interpretations = interpretation_result.data or []
        risks = risk_result.data or []
        ai_prediction = prediction_result.data or {}
        
        # Re-analyze risks with interpretations if needed
        if not risks and interpretations:
            risk_result = self.risk_analysis_agent.execute(cleaned_params, interpretations)
            self.agent_results.append(risk_result)
            risks = risk_result.data or []
        
        # STAGE 5: MULTI-AI COMPARISON - Compare all AIs and select best
        self.logger.info("🤖 Starting Multi-AI Comparison Agent...")
        all_ai_results = {}
        best_provider = None
        selection_reason = ""
        
        try:
            comparison_agent_result = await asyncio.wait_for(
                self.multi_ai_comparison_agent.execute(
                    interpretations,
                    risks,
                    cleaned_params,
                    patient_context
                ),
                timeout=45.0  # Longer timeout for parallel AI calls
            )
            self.agent_results.append(comparison_agent_result)
            
            if comparison_agent_result.success:
                comparison_result: ComparisonResult = comparison_agent_result.data
                recommendations = comparison_result.best_result
                all_ai_results = comparison_result.all_results
                best_provider = comparison_result.best_provider
                selection_reason = comparison_result.selection_reason
                
                self.logger.info(f"🏆 Selected best AI: {comparison_result.best_provider}")
            else:
                self.logger.warning("Multi-AI comparison failed, using standard LLM")
                llm_result = await asyncio.wait_for(
                    self.llm_recommendation_agent.execute(
                        interpretations, risks, cleaned_params, patient_context
                    ),
                    timeout=20.0
                )
                self.agent_results.append(llm_result)
                recommendations = llm_result.data or []
                all_ai_results = {}
        except asyncio.TimeoutError:
            self.logger.warning("Multi-AI comparison timed out, using fallback")
            recommendations = self._generate_quick_fallback_recommendations(cleaned_params, interpretations, risks)
            all_ai_results = {}
        except Exception as e:
            self.logger.error(f"Multi-AI comparison error: {e}")
            recommendations = self._generate_quick_fallback_recommendations(cleaned_params, interpretations, risks)
            all_ai_results = {}
        
        # Stage 6: Run prescriptions, medicines, and synthesis in PARALLEL
        try:
            prescription_task = asyncio.create_task(
                asyncio.to_thread(self.prescription_agent.execute, interpretations, risks, cleaned_params)
            )
            medicines_task = asyncio.create_task(
                asyncio.to_thread(self.medicines_agent.execute, interpretations, risks, cleaned_params)
            )
            synthesis_task = asyncio.create_task(
                asyncio.to_thread(self.synthesis_agent.execute, cleaned_params, interpretations, risks, recommendations)
            )
            
            prescription_result, medicines_result, synthesis_result = await asyncio.wait_for(
                asyncio.gather(prescription_task, medicines_task, synthesis_task),
                timeout=15.0
            )
        except asyncio.TimeoutError:
            self.logger.warning("Stage 6 parallel timeout, using fallbacks")
            from src.recommendation.recommendation_generator import generate_prescriptions, generate_medicines
            prescription_result = AgentResult(self.prescription_agent.name, False,
                generate_prescriptions(interpretations, risks, cleaned_params), "Timeout")
            medicines_result = AgentResult(self.medicines_agent.name, False,
                generate_medicines(interpretations, risks, cleaned_params), "Timeout")
            synthesis_result = AgentResult(self.synthesis_agent.name, False,
                f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks.", "Timeout")
        except Exception as e:
            self.logger.error(f"Stage 6 error: {str(e)}")
            from src.recommendation.recommendation_generator import generate_prescriptions, generate_medicines
            prescription_result = AgentResult(self.prescription_agent.name, False,
                generate_prescriptions(interpretations, risks, cleaned_params), str(e))
            medicines_result = AgentResult(self.medicines_agent.name, False,
                generate_medicines(interpretations, risks, cleaned_params), str(e))
            synthesis_result = AgentResult(self.synthesis_agent.name, False,
                f"Analysis of {len(cleaned_params)} parameters with {len(risks)} identified risks.", str(e))
        
        self.agent_results.extend([prescription_result, medicines_result, synthesis_result])
        
        prescriptions = prescription_result.data or []
        medicines = medicines_result.data or []
        synthesis = synthesis_result.data or ""
        
        overall_time = time.time() - overall_start
        
        # Build final report with multi-AI results
        report = AnalysisReport(
            status="success",
            extracted_parameters=self._format_parameters_with_descriptions(cleaned_params),
            interpretations=self._sort_interpretations(interpretations),
            risks=self._sort_risks(risks),
            ai_prediction=ai_prediction,
            recommendations=self._sort_recommendations(recommendations),
            medicines=medicines,
            prescriptions=self._sort_prescriptions(prescriptions),
            synthesis=synthesis,
            agent_results=self.agent_results,
            timestamp=datetime.now().isoformat(),
            best_provider=best_provider,
            selection_reason=selection_reason
        )
        
        # Add multi-AI comparison data to report
        if all_ai_results:
            report.multi_ai_results = all_ai_results
        
        self.logger.info(f"🎉 Multi-agent analysis WITH MULTI-AI COMPARISON completed in {overall_time:.2f}s")
        self._log_agent_summary(report)
        
        return report
    
    def _generate_quick_fallback_recommendations(self, params, interpretations, risks):
        """Generate recommendations quickly when LLM is unavailable."""
        recommendations = []
        
        # Priority-based recommendations
        if any("high" in str(r).lower() for r in risks):
            recommendations.append("⚠️ URGENT: Consult healthcare provider immediately due to elevated health risks")
        
        priority_params = ["glucose", "cholesterol", "blood_pressure", "hemoglobin"]
        for param in priority_params:
            if any(p.lower().startswith(param) for p in params.keys()):
                recommendations.append(f"📊 Monitor {param} levels regularly")
        
        if len(recommendations) == 0:
            recommendations = ["✅ Maintain current health regimen", "🏃 Regular exercise recommended", "💪 Healthy diet essential"]
        
        return recommendations[:5]
    
    def _format_parameters_with_descriptions(self, params: Dict) -> Dict:
        """Add clinical descriptions to parameters."""
        descriptions = {
            "glucose": "Blood sugar level", "glucose_fasting": "Fasting blood sugar",
            "cholesterol": "Total cholesterol", "hdl": "Good cholesterol (HDL)",
            "ldl": "Bad cholesterol (LDL)", "triglycerides": "Triglycerides level",
            "hemoglobin": "Red blood cell protein", "hematocrit": "RBC percentage",
            "white_blood_cells": "WBC count", "platelets": "Clotting cells",
            "albumin": "Protein level", "bilirubin": "Liver function",
            "alt": "Liver enzyme", "ast": "Liver enzyme", "creatinine": "Kidney function",
            "sodium": "Electrolyte", "potassium": "Electrolyte", "calcium": "Mineral",
            "phosphorus": "Mineral", "magnesium": "Mineral", "iron": "Mineral",
            "tsh": "Thyroid stimulating hormone", "t3": "Thyroid hormone", "t4": "Thyroid hormone"
        }
        
        formatted = {}
        for key, value in params.items():
            key_lower = key.lower().replace(" ", "_").replace("-", "_")
            desc = descriptions.get(key_lower, key.replace("_", " ").title())
            formatted[desc] = value
        
        return formatted
    
    def _sort_interpretations(self, interpretations: List[str]) -> List[str]:
        """Sort interpretations by severity and importance."""
        if not interpretations:
            return []
        
        def severity_score(text: str) -> tuple:
            text_lower = text.lower()
            # Return (severity_level, text) for sorting
            if any(w in text_lower for w in ["critical", "severe", "emergency"]):
                return (0, text)  # Highest priority
            elif any(w in text_lower for w in ["abnormal", "high", "low", "elevated"]):
                return (1, text)
            elif any(w in text_lower for w in ["normal", "regular"]):
                return (2, text)
            else:
                return (3, text)
        
        return sorted(interpretations, key=severity_score)
    
    def _sort_risks(self, risks: List[str]) -> List[str]:
        """Sort risks by severity level."""
        if not risks:
            return []
        
        def risk_score(text: str) -> tuple:
            text_lower = text.lower()
            # Return (severity_level, text) for sorting
            if any(w in text_lower for w in ["critical", "severe", "immediate"]):
                return (0, text)
            elif any(w in text_lower for w in ["high", "significant"]):
                return (1, text)
            elif any(w in text_lower for w in ["moderate", "medium"]):
                return (2, text)
            elif any(w in text_lower for w in ["low", "minor"]):
                return (3, text)
            else:
                return (4, text)
        
        return sorted(risks, key=risk_score)
    
    def _sort_recommendations(self, recommendations: List[str]) -> List[str]:
        """Sort recommendations by priority and urgency."""
        if not recommendations:
            return []
        
        def priority_score(text: str) -> tuple:
            text_lower = text.lower()
            # Return (priority_level, text) for sorting
            if any(w in text_lower for w in ["immediate", "urgent", "emergency"]):
                return (0, text)
            elif any(w in text_lower for w in ["consult", "doctor", "provider", "medical"]):
                return (1, text)
            elif any(w in text_lower for w in ["daily", "regular", "monitor"]):
                return (2, text)
            else:
                return (3, text)
        
        return sorted(recommendations, key=priority_score)
    
    def _sort_prescriptions(self, prescriptions: List[str]) -> List[str]:
        """Sort prescriptions by type and dosage."""
        if not prescriptions:
            return []
        
        def prescription_score(text: str) -> tuple:
            text_lower = text.lower()
            # Return (type_order, text) for sorting
            if "urgent" in text_lower or "stat" in text_lower:
                return (0, text)
            elif "medication" in text_lower or "drug" in text_lower:
                return (1, text)
            elif "supplement" in text_lower or "vitamin" in text_lower:
                return (2, text)
            else:
                return (3, text)
        
        return sorted(prescriptions, key=prescription_score)
    
    def _create_failed_report(self, initial_error: AgentResult) -> AnalysisReport:
        """Create a failed analysis report."""
        return AnalysisReport(
            status="failed",
            extracted_parameters={},
            interpretations=[],
            risks=[],
            ai_prediction={},
            recommendations=["Consult healthcare provider for personalized advice"],
            medicines=[],
            prescriptions=[],
            synthesis="",
            agent_results=self.agent_results,
            timestamp=datetime.now().isoformat()
        )
    
    def _log_agent_summary(self, report: AnalysisReport) -> None:
        """Log summary of agent results."""
        self.logger.info("=" * 60)
        self.logger.info("MULTI-AGENT ANALYSIS SUMMARY")
        self.logger.info("=" * 60)
        
        for result in report.agent_results:
            status = "✓ SUCCESS" if result.success else "✗ FAILED"
            self.logger.info(f"{status} | {result.agent_name} ({result.execution_time:.2f}s)")
            if result.error:
                self.logger.warning(f"  Error: {result.error}")
        
        self.logger.info("=" * 60)
        self.logger.info(f"Total Parameters: {len(report.extracted_parameters)}")
        self.logger.info(f"Interpretations: {len(report.interpretations)}")
        self.logger.info(f"Identified Risks: {len(report.risks)}")
        self.logger.info(f"Recommendations: {len(report.recommendations)}")
        self.logger.info(f"Prescriptions: {len(report.prescriptions)}")
        self.logger.info("=" * 60)
