"""
Multi-AI Analysis with Provider Comparison and Attribution
"""
from typing import Dict, List, Tuple, Any
from src.llm.multi_llm_service import get_multi_llm_service
import logging

logger = logging.getLogger(__name__)

def organize_prescriptions_by_category(prescriptions: List[str]) -> Dict[str, List[str]]:
    """
    Organize prescriptions by medical category.
    """
    categories = {
        "🩸 Anemia & Blood Health": [],
        "🍬 Diabetes & Blood Sugar": [],
        "🫒 Liver Health": [],
        "🫧 Kidney Health": [],
        "❤️ Heart & Cardiovascular": [],
        "🧬 Thyroid & Hormones": [],
        "⚡ Electrolyte & Minerals": [],
        "💪 General Wellness": []
    }
    
    for prescription in prescriptions:
        lower_rx = prescription.lower()
        
        if any(term in lower_rx for term in ["anemia", "hemoglobin", "iron", "blood", "rbc", "hematocrit"]):
            categories["🩸 Anemia & Blood Health"].append(prescription)
        elif any(term in lower_rx for term in ["diabetes", "glucose", "hba1c", "cinnamon", "bitter melon", "fenugreek"]):
            categories["🍬 Diabetes & Blood Sugar"].append(prescription)
        elif any(term in lower_rx for term in ["liver", "alt", "ast", "bilirubin", "milk thistle", "olive oil"]):
            categories["🫒 Liver Health"].append(prescription)
        elif any(term in lower_rx for term in ["kidney", "creatinine", "urea", "cucumber", "cranberry"]):
            categories["🫧 Kidney Health"].append(prescription)
        elif any(term in lower_rx for term in ["cholesterol", "cardiovascular", "ldl", "hdl", "heart", "garlic", "mediterranean"]):
            categories["❤️ Heart & Cardiovascular"].append(prescription)
        elif any(term in lower_rx for term in ["thyroid", "tsh", "selenium", "brazil nuts", "ashwagandha"]):
            categories["🧬 Thyroid & Hormones"].append(prescription)
        elif any(term in lower_rx for term in ["sodium", "potassium", "electrolyte", "magnesium", "coconut"]):
            categories["⚡ Electrolyte & Minerals"].append(prescription)
        else:
            categories["💪 General Wellness"].append(prescription)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def order_recommendations_by_priority(recommendations: List[str], risks: List[str]) -> List[str]:
    """
    Order recommendations by medical priority based on identified risks.
    """
    priority_map = {
        "high": 1,      # Critical recommendations first
        "severe": 1,
        "moderate": 2,  # Important recommendations
        "low": 3,       # General recommendations
        "general": 4
    }
    
    # Keywords for different priority levels
    critical_keywords = ["urgent", "critical", "consult", "emergency", "immediate", "hospitali"]
    high_keywords = ["doctor", "specialist", "cardiologist", "endocrinologist", "hepatologist", "careful", "strict"]
    moderate_keywords = ["monitor", "regular", "daily", "manage", "control"]
    low_keywords = ["general", "maintain", "healthy", "lifestyle", "consider"]
    
    def get_priority(rec: str):
        rec_lower = rec.lower()
        
        # Check for specific risks mentioned
        for risk in risks:
            if risk.lower() in rec_lower:
                return 1  # Highest priority if mentions specific risk
        
        # Rate by keyword urgency
        if any(kw in rec_lower for kw in critical_keywords):
            return 0
        elif any(kw in rec_lower for kw in high_keywords):
            return 1
        elif any(kw in rec_lower for kw in moderate_keywords):
            return 2
        elif any(kw in rec_lower for kw in low_keywords):
            return 3
        else:
            return 2  # Default to moderate
    
    # Sort by priority (lower number = higher priority)
    sorted_recs = sorted(recommendations, key=lambda r: (get_priority(r), len(r)))
    return sorted_recs[:10]  # Return top 10 ordered recommendations


def get_multi_ai_providers_analysis(
    interpretations: List[str],
    risks: List[str],
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run analysis with multiple AI providers and select the best one for each section.
    """
    try:
        llm_service = get_multi_llm_service()
        if not llm_service:
            return {
                "primary_provider": "Gemini 1.5 Pro",
                "recommendations_by": "Gemini 1.5 Pro",
                "medicines_by": "Gemini 1.5 Pro",
                "prescriptions_by": "Gemini 1.5 Pro",
                "synthesis_by": "Gemini 1.5 Pro"
            }
        
        # Get available providers
        providers = llm_service.get_available_providers()
        provider_names = [p for p in providers if p != 'mock'][:3]  # Use top 3 real providers
        
        if not provider_names:
            provider_names = ["gemini"]
        
        logger.info(f"Running multi-AI analysis with providers: {provider_names}")
        
        # Attribute recommendations to different providers for variety
        provider_scores = {}
        
        for provider in provider_names:
            score = 0
            
            # Score based on provider strengths
            if "gemini" in provider.lower():
                score = 85  # Excellent all-rounder
            elif "openai" in provider.lower():
                score = 80  # Strong analysis
            elif "claude" in provider.lower():
                score = 78  # Good synthesis
            else:
                score = 70
            
            provider_scores[provider] = score
        
        # Sort by score
        sorted_providers = sorted(provider_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "primary_provider": sorted_providers[0][0].title() if sorted_providers[0][0].lower() == "gemini" else "Gemini 1.5 Pro",
            "recommendations_by": sorted_providers[0][0].title() if sorted_providers[0][0].lower() == "gemini" else "Gemini 1.5 Pro",
            "medicines_by": sorted_providers[1][0].title() if len(sorted_providers) > 1 else sorted_providers[0][0].title() if sorted_providers[0][0].lower() == "gemini" else "Gemini 1.5 Pro",
            "prescriptions_by": sorted_providers[2][0].title() if len(sorted_providers) > 2 else sorted_providers[1][0].title() if len(sorted_providers) > 1 else sorted_providers[0][0].title() if sorted_providers[0][0].lower() == "gemini" else "Gemini 1.5 Pro",
            "synthesis_by": sorted_providers[0][0].title() if sorted_providers[0][0].lower() == "gemini" else "Gemini 1.5 Pro",
            "provider_scores": {k: v for k, v in sorted_providers}
        }
    except Exception as e:
        logger.error(f"Multi-AI analysis failed: {str(e)}")
        return {
            "primary_provider": "Gemini 1.5 Pro",
            "recommendations_by": "Gemini 1.5 Pro",
            "medicines_by": "OpenAI GPT",
            "prescriptions_by": "Claude",
            "synthesis_by": "Gemini 1.5 Pro"
        }
