"""Sample medical data for demonstrations and fallbacks."""

# Healthy sample blood report
HEALTHY_SAMPLE = {
    "hemoglobin": 13.5,
    "glucose": 95,
    "cholesterol": 180,
    "hdl": 55,
    "ldl": 100,
    "triglycerides": 120,
    "creatinine": 0.9,
    "urea": 30,
    "bilirubin_total": 0.7,
    "ast": 28,
    "alt": 25,
    "alp": 85,
    "sodium": 140,
    "potassium": 4.2,
    "calcium": 9.2,
    "albumin": 4.0,
    "wbc": 7.2,
    "platelets": 250,
}

# Pre-diabetic sample
PREDIABETIC_SAMPLE = {
    "hemoglobin": 12.8,
    "glucose": 115,
    "cholesterol": 210,
    "hdl": 42,
    "ldl": 135,
    "triglycerides": 180,
    "creatinine": 0.95,
    "urea": 32,
    "bilirubin_total": 0.8,
    "ast": 32,
    "alt": 38,
    "alp": 95,
    "sodium": 139,
    "potassium": 4.1,
    "calcium": 8.9,
    "albumin": 3.8,
    "wbc": 7.8,
    "platelets": 230,
}

# High cholesterol sample
HYPERLIPIDEMIA_SAMPLE = {
    "hemoglobin": 13.2,
    "glucose": 100,
    "cholesterol": 260,
    "hdl": 38,
    "ldl": 170,
    "triglycerides": 320,
    "creatinine": 0.88,
    "urea": 28,
    "bilirubin_total": 0.6,
    "ast": 25,
    "alt": 22,
    "alp": 78,
    "sodium": 141,
    "potassium": 4.3,
    "calcium": 9.5,
    "albumin": 4.1,
    "wbc": 6.8,
    "platelets": 270,
}

# Anemia sample
ANEMIA_SAMPLE = {
    "hemoglobin": 9.5,
    "glucose": 92,
    "cholesterol": 175,
    "hdl": 50,
    "ldl": 105,
    "triglycerides": 110,
    "creatinine": 0.85,
    "urea": 25,
    "bilirubin_total": 1.2,
    "ast": 35,
    "alt": 28,
    "alp": 90,
    "sodium": 138,
    "potassium": 3.8,
    "calcium": 8.5,
    "albumin": 3.5,
    "wbc": 6.2,
    "platelets": 180,
}

SAMPLE_REPORTS = {
    "healthy": HEALTHY_SAMPLE,
    "prediabetic": PREDIABETIC_SAMPLE,
    "high_cholesterol": HYPERLIPIDEMIA_SAMPLE,
    "anemia": ANEMIA_SAMPLE,
}


def get_sample_report(report_type: str = "healthy") -> dict:
    """Get a sample blood report by type."""
    return SAMPLE_REPORTS.get(report_type.lower(), HEALTHY_SAMPLE).copy()


def get_all_sample_types() -> list:
    """Get list of available sample report types."""
    return list(SAMPLE_REPORTS.keys())
