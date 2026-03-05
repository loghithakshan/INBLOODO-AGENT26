def clean_and_structure_data(params: dict) -> dict:
    """Clean and structure medical parameters with flexible validation."""
    import logging
    logger = logging.getLogger(__name__)
    
    if not params:
        logger.warning("No parameters provided")
        return {}
    
    # Define allowed blood parameters with reasonable ranges
    allowed_params = {
        'hemoglobin': (5, 20),  # g/dL
        'glucose': (40, 500),  # mg/dL
        'cholesterol': (50, 400),  # mg/dL
        'ldl': (10, 250),  # mg/dL
        'hdl': (10, 150),  # mg/dL
        'triglycerides': (0, 1000),  # mg/dL
        'creatinine': (0.4, 5),  # mg/dL
        'potassium': (2, 8),  # mEq/L
        'sodium': (130, 155),  # mEq/L
        'calcium': (6, 11),  # mg/dL
        'phosphorus': (2, 5),  # mg/dL
        'albumin': (2, 5.5),  # g/dL
        'total_protein': (6, 8.5),  # g/dL
        'bilirubin': (0.1, 3),  # mg/dL
        'ast': (10, 200),  # U/L
        'alt': (10, 200),  # U/L
        'alkaline_phosphatase': (20, 200),  # U/L
        'urea': (7, 50),  # mg/dL
        'wbc': (4, 15),  # 10^3/uL
        'rbc': (3, 7),  # 10^6/uL
        'hemoglobin_value': (5, 20),  # g/dL
        'hematocrit': (20, 55),  # %
        'platelets': (100, 500),  # 10^3/uL
        'mch': (25, 35),  # pg
        'mcv': (75, 100),  # fL
    }
    
    cleaned = {}
    for key, value in params.items():
        key_orig = key
        key = key.lower().strip().replace(' ', '_').replace('-', '_')
        
        # Try to convert string values to numbers
        if isinstance(value, str):
            try:
                value = float(value)
            except (ValueError, TypeError):
                logger.debug(f"Skipping {key_orig}: cannot convert '{value}' to number")
                continue
        
        # Accept numeric values
        if isinstance(value, (int, float)):
            # Check if it's a known parameter with range validation
            if key in allowed_params:
                min_val, max_val = allowed_params[key]
                if min_val <= value <= max_val:
                    cleaned[key] = float(value)
                else:
                    logger.warning(f"Parameter {key} value {value} outside range [{min_val}, {max_val}]")
            else:
                # Accept unknown parameters if they're reasonable (0 to 100000)
                if 0 <= value <= 100000:
                    cleaned[key] = float(value)
                else:
                    logger.debug(f"Skipping {key}: value {value} outside reasonable range")
    
    if cleaned:
        logger.info(f"Cleaned {len(cleaned)} parameters from {len(params)} input parameters")
    else:
        logger.error(f"No valid parameters after cleaning from input: {list(params.keys())}")
    
    return cleaned