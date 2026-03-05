"""
Enhanced Image Extraction Module
Improved parameter extraction from medical images with smart fallbacks.
"""
import logging
from fastapi import UploadFile
import tempfile
import os
from PIL import Image, ImageFilter, ImageEnhance
import re

logger = logging.getLogger(__name__)


def preprocess_medical_image(image_path: str) -> Image.Image:
    """
    Advanced preprocessing for medical document images.
    Optimizes image for OCR text extraction.
    """
    try:
        img = Image.open(image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Enhance contrast for better text visibility
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Enhance brightness if needed
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # Apply sharpening filter
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.SHARPEN)
        
        # Resize if too small (helps with OCR accuracy)
        width, height = img.size
        if width < 800 or height < 600:
            scale_factor = max(800 / width, 600 / height)
            new_size = (int(width * scale_factor), int(height * scale_factor))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        return img
    except Exception as e:
        logger.warning(f"Preprocessing failed: {str(e)}, using original image")
        return Image.open(image_path)


def extract_numbers_from_text(text: str) -> dict:
    """
    Extract medical parameters using regex patterns.
    Fallback when OCR produces poor results.
    """
    extracted = {}
    
    # Pattern definitions for common blood parameters with their variations
    patterns = {
        'hemoglobin': r'(?:hemoglobin|hb|hgb)[\s:=-]*([0-9]+\.?[0-9]*)',
        'glucose': r'(?:glucose|blood\s?sugar|fbs)[\s:=-]*([0-9]+\.?[0-9]*)',
        'cholesterol': r'(?:cholesterol|total\s?cholesterol)[\s:=-]*([0-9]+\.?[0-9]*)',
        'triglycerides': r'(?:triglycerides|tg)[\s:=-]*([0-9]+\.?[0-9]*)',
        'hdl': r'(?:hdl|hdl\s?cholesterol)[\s:=-]*([0-9]+\.?[0-9]*)',
        'ldl': r'(?:ldl|ldl\s?cholesterol)[\s:=-]*([0-9]+\.?[0-9]*)',
        'creatinine': r'(?:creatinine|crea)[\s:=-]*([0-9]+\.?[0-9]*)',
        'urea': r'(?:urea|bun|blood\s?urea)[\s:=-]*([0-9]+\.?[0-9]*)',
        'bilirubin': r'(?:bilirubin|total\s?bilirubin)[\s:=-]*([0-9]+\.?[0-9]*)',
        'wbc': r'(?:wbc|white\s?blood\s?cell)[\s:=-]*([0-9]+\.?[0-9]*)',
        'platelets': r'(?:platelets|plt)[\s:=-]*([0-9]+\.?[0-9]*)',
        'rbc': r'(?:rbc|red\s?blood\s?cell)[\s:=-]*([0-9]+\.?[0-9]*)',
        'hematocrit': r'(?:hematocrit|hct)[\s:=-]*([0-9]+\.?[0-9]*)',
        'ast': r'(?:ast|aspartate|sgot)[\s:=-]*([0-9]+\.?[0-9]*)',
        'alt': r'(?:alt|alanine|sgpt)[\s:=-]*([0-9]+\.?[0-9]*)',
        'alp': r'(?:alp|alkaline\s?phosphatase)[\s:=-]*([0-9]+\.?[0-9]*)',
        'sodium': r'(?:sodium|na)[\s:=-]*([0-9]+\.?[0-9]*)',
        'potassium': r'(?:potassium|k)[\s:=-]*([0-9]+\.?[0-9]*)',
        'calcium': r'(?:calcium|ca)[\s:=-]*([0-9]+\.?[0-9]*)',
    }
    
    text_lower = text.lower()
    
    for param, pattern in patterns.items():
        try:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                value_str = match.group(1)
                value = float(value_str)
                # Validate against reasonable ranges
                if 0 <= value <= 100000:
                    extracted[param] = value
                    logger.debug(f"Pattern extracted {param}: {value}")
        except (ValueError, IndexError) as e:
            logger.debug(f"Failed to extract {param}: {str(e)}")
            continue
    
    return extracted


def smart_fallback_extraction(ocr_text: str, image_analysis: dict) -> dict:
    """
    Smart fallback extraction when OCR confidence is low.
    Combines multiple extraction strategies.
    """
    extracted = {}
    
    # Strategy 1: Use existing parameter extraction
    if image_analysis.get('extracted_parameters'):
        extracted.update(image_analysis['extracted_parameters'])
    
    # Strategy 2: Regex-based extraction from OCR text
    regex_params = extract_numbers_from_text(ocr_text)
    extracted.update(regex_params)
    
    logger.info(f"Fallback extraction found {len(extracted)} parameters")
    return extracted


def validate_extracted_parameters(params: dict) -> dict:
    """
    Validate and clean extracted parameters.
    Removes invalid values and normalizes keys.
    """
    validated = {}
    
    for key, value in params.items():
        try:
            # Normalize key
            normalized_key = key.lower().strip().replace(' ', '_').replace('-', '_')
            
            # Convert to float
            if isinstance(value, str):
                clean_value = value.strip().replace(',', '.')
                value = float(clean_value)
            elif not isinstance(value, (int, float)):
                continue
            
            # Validate range (medical values are typically 0-10000)
            if 0 <= value <= 100000:
                validated[normalized_key] = float(value)
        except (ValueError, TypeError):
            logger.debug(f"Skipping invalid parameter {key}={value}")
            continue
    
    return validated
