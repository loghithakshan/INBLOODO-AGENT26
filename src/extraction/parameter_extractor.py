import re
import logging
from src.extraction.medical_schema import MEDICAL_SCHEMA

logger = logging.getLogger(__name__)

def extract_parameters_from_text(text: str) -> dict:
    """
    Extract medical parameters from text using improved regex patterns.
    Handles various number formats and units.
    Uses multiple strategies to maximize extraction.
    """
    if not text or not isinstance(text, str):
        logger.warning("No text provided for extraction")
        return {}
        
    text_lower = text.lower()
    extracted = {}
    found_count = 0
    attempted_count = 0

    for parameter, aliases in MEDICAL_SCHEMA.items():
        for alias in aliases:
            attempted_count += 1
            
            # Strategy 1: Pattern with colon, equals, or dash
            pattern_strict = rf"(?:\b|^){re.escape(alias)}\s*[:=\-]\s*([0-9]{{1,3}}(?:,[0-9]{{3}})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)"
            match = re.search(pattern_strict, text_lower)
            
            if not match:
                # Strategy 2: Pattern without required colon (flexible spacing)
                pattern_lax = rf"(?:\b|^){re.escape(alias)}\s+([0-9]{{1,3}}(?:,[0-9]{{3}})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)(?:\s|$)"
                match = re.search(pattern_lax, text_lower)
            
            if not match:
                # Strategy 3: Very lenient with numbers on same line after parameter
                pattern_lenient = rf"{re.escape(alias)}\s*(?:is|=|:)?\s*([0-9]+(?:[.,][0-9]+)?)"
                match = re.search(pattern_lenient, text_lower)
            
            if match:
                try:
                    value_str = match.group(1)
                    # Remove commas and replace European decimal separator
                    value_str = value_str.replace(',', '.') if ',' in value_str else value_str
                    value_float = float(value_str)
                    
                    # Validate against reasonable ranges
                    if 0 <= value_float <= 10000:  # Most medical values are in this range
                        extracted[parameter] = value_float
                        found_count += 1
                        logger.debug(f"Found {parameter}: {value_float}")
                        break
                except (ValueError, AttributeError) as e:
                    logger.debug(f"Failed to parse value for {alias}: {str(e)}")
                    continue
    
    logger.info(f"Parameter extraction: Found {found_count} parameters (attempted {attempted_count} patterns)")
    return extracted
