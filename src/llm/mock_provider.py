"""
Mock/Offline LLM Provider - Works without API keys for testing and fallback.
Generates intelligent recommendations based on medical parameters and risks.
"""

import logging
from typing import List, Dict, Any, Optional

from src.llm.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class MockLLMProvider(LLMProvider):
    """Mock LLM provider that generates recommendations without external API calls."""
    
    def __init__(self):
        self.name = "Mock LLM (Offline)"
        self.available = True  # Always available
        self.model_name = "mock-v1"
    
    def initialize(self) -> bool:
        """Mock provider is always initialized."""
        logger.info(f"{self.name} LLM provider initialized")
        return True
    
    def is_available(self) -> bool:
        """Mock provider is always available."""
        return True
    
    def generate_recommendations(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate intelligent recommendations based on health data."""
        recommendations = []
        
        # Analyze parameters and build context
        param_analysis = self._analyze_parameters(parameters)
        
        # Priority 1: Critical risks
        if risks:
            for risk in risks[:3]:  # Top 3 risks
                if "diabetes" in risk.lower() or "glucose" in risk.lower():
                    recommendations.extend([
                        "1. Implement strict dietary control: avoid refined sugars and simple carbohydrates",
                        "2. Increase physical activity to at least 150 minutes per week of moderate exercise",
                        "3. Monitor blood glucose levels regularly and log results"
                    ])
                elif "cardiovascular" in risk.lower() or "hypertension" in risk.lower():
                    recommendations.extend([
                        "1. Reduce sodium intake to less than 2,300mg per day",
                        "2. Increase aerobic exercise: brisk walking, swimming, or cycling",
                        "3. Consider heart-healthy Mediterranean diet with omega-3 fatty acids"
                    ])
                elif "cholesterol" in risk.lower() or "lipid" in risk.lower():
                    recommendations.extend([
                        "1. Increase soluble fiber intake: oats, legumes, apple, beans",
                        "2. Limit saturated fats and eliminate trans fats",
                        "3. Include fatty fish (salmon, mackerel) 2-3 times per week"
                    ])
                elif "kidney" in risk.lower() or "creatinine" in risk.lower():
                    recommendations.extend([
                        "1. Maintain adequate hydration: drink 8-10 glasses of water daily",
                        "2. Limit protein intake as advised by nephrologist",
                        "3. Monitor blood pressure closely and manage sodium intake"
                    ])
                elif "liver" in risk.lower() or "bilirubin" in risk.lower():
                    recommendations.extend([
                        "1. Avoid alcohol completely",
                        "2. Maintain healthy weight through balanced nutrition",
                        "3. Get hepatitis vaccines if not already immunized"
                    ])
        
        # Priority 2: Parameter-specific recommendations
        if param_analysis.get("glucose_elevated"):
            recs = [
                "4. Reduce refined carbohydrates and increase whole grains",
                "5. Time meals and snacks consistently throughout the day",
                "6. Consult with a dietitian for personalized meal planning"
            ]
            if "4." not in "\n".join(recommendations):
                recommendations.extend(recs)
        
        if param_analysis.get("hemoglobin_low"):
            recs = [
                "4. Increase iron-rich foods: red meat, spinach, lentils, fortified cereals",
                "5. Enhance iron absorption with vitamin C sources: citrus fruits, tomatoes",
                "6. Consider iron supplementation if recommended by physician"
            ]
            if "4." not in "\n".join(recommendations):
                recommendations.extend(recs)
        
        if param_analysis.get("cholesterol_elevated"):
            recs = [
                "4. Switch to plant-based oils: olive, avocado, and canola oil",
                "5. Include nuts and seeds daily: almonds, walnuts, flax seeds",
                "6. Aim for 25-30g of fiber daily from whole grain sources"
            ]
            if "4." not in "\n".join(recommendations):
                recommendations.extend(recs)
        
        # General lifestyle recommendations
        general_recs = [
            "7. 💤 Establish consistent sleep schedule: 7-9 hours nightly",
            "8. 🧘 Practice stress management: meditation, yoga, or deep breathing",
            "9. 🚶 Take daily walks for at least 30 minutes",
            "10. 📅 Schedule regular follow-up health check-ups (every 3-6 months)",
            "11. 💊 Take medications as prescribed and maintain treatment compliance",
            "12. 📝 Keep a health journal to track symptoms and progress"
        ]
        
        recommendations.extend(general_recs)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in recommendations:
            # Extract key part for duplicate detection
            key = rec.split(":")[0].split("-")[-1].strip()
            if key not in seen:
                seen.add(key)
                unique_recs.append(rec)
        
        logger.info(f"Generated {len(unique_recs)} recommendations from {self.name}")
        return unique_recs[:12]  # Return up to 12 recommendations
    
    def generate_text(self, prompt: str, max_tokens: int = 2048) -> str:
        """Generate text response based on prompt."""
        # Simple text generation for general prompts
        if "recommendation" in prompt.lower():
            return "Based on the provided health data, the patient should focus on lifestyle modifications including regular exercise, balanced diet, stress management, and consistent medical monitoring. All recommendations should be implemented gradually and discussed with healthcare providers."
        
        return "Unable to generate detailed response for this prompt. Please provide health-related parameters for better recommendations."
    
    def _analyze_parameters(self, parameters: Dict[str, Any]) -> Dict[str, bool]:
        """Analyze medical parameters to identify abnormalities."""
        analysis = {}
        
        # Glucose analysis
        glucose = parameters.get("glucose", 0)
        analysis["glucose_elevated"] = glucose > 126  # Fasting threshold
        analysis["glucose_low"] = glucose < 70
        
        # Hemoglobin analysis
        hemoglobin = parameters.get("hemoglobin", 0)
        analysis["hemoglobin_low"] = hemoglobin < 12.0  # Lower threshold for general population
        analysis["hemoglobin_high"] = hemoglobin > 17.5
        
        # Cholesterol analysis
        cholesterol = parameters.get("cholesterol", 0)
        analysis["cholesterol_elevated"] = cholesterol > 200
        
        # LDL analysis
        ldl = parameters.get("ldl", 0)
        analysis["ldl_elevated"] = ldl > 100
        
        # HDL analysis
        hdl = parameters.get("hdl", 0)
        analysis["hdl_low"] = hdl < 40
        
        # Triglycerides analysis
        triglycerides = parameters.get("triglycerides", 0)
        analysis["triglycerides_elevated"] = triglycerides > 150
        
        # Creatinine analysis
        creatinine = parameters.get("creatinine", 0)
        analysis["creatinine_elevated"] = creatinine > 1.2
        
        return analysis
    
    def _parse_llm_response(self, response_text: str) -> List[str]:
        """Parse response into clean list of recommendations."""
        recommendations = []
        
        # Split by numbered items or bullet points
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and any(line.startswith(f"{i}.") for i in range(1, 20)):
                recommendations.append(line)
            elif line.startswith("-") or line.startswith("•"):
                recommendations.append(line.lstrip("-•").strip())
        
        return recommendations if recommendations else [response_text]
    
    def _build_recommendation_prompt(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build prompt for recommendations (for reference)."""
        return f"Generate health recommendations for: {risks}"
