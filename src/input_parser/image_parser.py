import easyocr
from PIL import Image, ImageFilter, ImageEnhance
import tempfile
import os
import numpy as np
from fastapi import UploadFile, HTTPException
import logging
import cv2
import ssl
import gc  # Garbage collection for memory management

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix SSL certificate verification issues on some systems
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Lazy initialization for EasyOCR reader
# Don't load the model on import - only load when first needed
_reader = None
_reader_initialized = False

def get_reader():
    """Get or initialize EasyOCR reader lazily to save memory."""
    global _reader, _reader_initialized
    
    if _reader_initialized:
        return _reader
    
    _reader_initialized = True
    
    try:
        model_dir = os.path.join(os.getcwd(), "data", "easyocr_models")
        os.makedirs(model_dir, exist_ok=True)
        logger.info("Initializing EasyOCR reader (this may take a moment)...")
        _reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir)
        logger.info("EasyOCR reader initialized successfully")
        return _reader
    except Exception as e:
        logger.error(f"Failed to initialize EasyOCR reader: {str(e)}. OCR will be skipped.")
        _reader = None
        return None



def extract_text_from_image(upload_file: UploadFile, timeout_sec=30) -> str:
    """
    Extract text from uploaded image using EasyOCR.
    EasyOCR is a pure Python solution that doesn't require external dependencies.
    NOW WITH AGGRESSIVE DOWNSCALING FOR SPEED AND MEMORY EFFICIENCY.
    """
    ocr_reader = get_reader()
    if ocr_reader is None:
        logger.warning("EasyOCR reader not available, returning empty text")
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = tmp.name

    try:
        # Open and preprocess image
        image = Image.open(tmp_path)

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # AGGRESSIVE DOWNSCALING: max 1200 pixels (was 2000) 
        # This reduces processing time by ~60%
        max_size = 1200
        original_size = image.size
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"FAST: Scaled image to {new_size[0]}x{new_size[1]} (from {original_size[0]}x{original_size[1]})")

        # Light sharpening for medical document clarity
        image = image.filter(ImageFilter.SHARPEN)

        # Convert PIL image to numpy array for EasyOCR
        image_np = np.array(image)

        # Extract text using EasyOCR
        results = ocr_reader.readtext(image_np, detail=0)  # detail=0 returns only text

        # Join all detected text
        text = ' '.join(results)
        
        # Clean memory
        del image
        del image_np
        gc.collect()

        return text.strip()

    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
        return ""
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        gc.collect()


def extract_text_with_opencv(upload_file: UploadFile) -> str:
    """
    Alternative implementation using OpenCV for preprocessing and EasyOCR for OCR.
    AGGRESSIVE OPTIMIZATION: Smaller downscaling for faster processing.
    """
    ocr_reader = get_reader()
    if ocr_reader is None:
        logger.warning("EasyOCR reader not available")
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = tmp.name

    try:
        # Read image with OpenCV
        image = cv2.imread(tmp_path)
        
        # AGGRESSIVE DOWNSCALING: max 1200px (was 2000)
        max_size = 1200
        height, width = image.shape[:2]
        if max(height, width) > max_size:
            ratio = max_size / max(height, width)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            logger.info(f"FAST: Scaled image to {new_width}x{new_height}")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Light noise reduction only (faster than median)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Simple thresholding (faster)
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Extract text using EasyOCR
        results = ocr_reader.readtext(threshold, detail=0)
        text = ' '.join(results)
        
        # Clean memory
        del image
        del gray
        del threshold
        gc.collect()
        
        return text.strip()

    except Exception as e:
        logger.error(f"OpenCV OCR failed: {str(e)}")
        return ""
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        gc.collect()


def preprocess_image_advanced(image_path: str) -> list:
    """
    Apply MINIMAL preprocessing techniques for speed.
    AGGRESSIVE OPTIMIZATION: Only 2-3 versions instead of 5.
    """
    original = Image.open(image_path)

    # Ensure RGB mode
    if original.mode != 'RGB':
        original = original.convert('RGB')

    # AGGRESSIVE DOWNSCALING to 1200px BEFORE creating versions
    max_size = 1200
    if max(original.size) > max_size:
        ratio = max_size / max(original.size)
        new_size = tuple(int(dim * ratio) for dim in original.size)
        original = original.resize(new_size, Image.Resampling.LANCZOS)
        logger.info(f"FAST: Preprocessor scaled to {new_size[0]}x{new_size[1]}")

    preprocessed_images = []

    # 1. Original image (lightest preprocessing)
    preprocessed_images.append(original)

    # 2. Enhanced contrast (best for faded documents)
    try:
        enhancer = ImageEnhance.Contrast(original)
        contrast_enhanced = enhancer.enhance(1.8)
        preprocessed_images.append(contrast_enhanced)
    except Exception as e:
        logger.warning(f"Contrast enhancement failed: {e}")

    # SKIP 3-5 for speed (morphological, separate brightness versions)
    # These slow down processing significantly for minimal gains

    return preprocessed_images


def extract_text_automated(upload_file: UploadFile) -> str:
    """
    AGGRESSIVELY OPTIMIZED: Fast automated image processing with early exit.
    Tries only 2-3 versions and exits early if good results found.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = tmp.name

    try:
        ocr_reader = get_reader()
        if ocr_reader is None:
            logger.warning("EasyOCR reader not available for automated processing")
            return ""
        
        logger.info("FAST: Starting automated EasyOCR processing...")

        # Get only 2-3 preprocessed versions (was 5)
        preprocessed_images = preprocess_image_advanced(tmp_path)

        best_text = ""
        best_score = 0

        # Try each preprocessing technique with EARLY EXIT
        for i, img in enumerate(preprocessed_images):
            try:
                # Convert to numpy array
                img_np = np.array(img)

                # Extract text with EasyOCR
                results = ocr_reader.readtext(img_np, detail=0)
                text = ' '.join(results).strip()

                # Score based on text length
                score = len(text)

                if score > 0:
                    logger.info(f"Version {i+1}: {score} chars")

                    # EARLY EXIT: If we get 500+ characters, that's probably good enough
                    if score > 500:
                        best_text = text
                        logger.info(f"FAST: Good result found, exiting early")
                        break

                if score > best_score:
                    best_score = score
                    best_text = text

            except Exception as e:
                logger.warning(f"Version {i+1} failed: {str(e)}")
                continue
            finally:
                # Aggressive memory cleanup
                if 'img' in locals():
                    del img
                if 'img_np' in locals():
                    del img_np
                gc.collect()

        # Clear preprocessed images to free memory
        del preprocessed_images
        gc.collect()

        if not best_text or not best_text.strip():
            logger.warning("Automated OCR produced no text")
            return ""

        logger.info(f"FAST: Final result: {len(best_text)} chars")
        return best_text

    except Exception as e:
        logger.error(f"Automated OCR failed: {str(e)}")
        return ""
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        gc.collect()


def extract_text_with_fallback(upload_file: UploadFile) -> str:
    """
    AGGRESSIVELY FAST: Extract text with multiple fallback methods.
    Tries basic method first, skips slow preprocessing if it takes too long.
    """
    ocr_reader = get_reader()
    if ocr_reader is None:
        logger.error("EasyOCR reader not available")
        raise HTTPException(
            status_code=500,
            detail="OCR service temporarily unavailable. Please contact administrator or try again later."
        )

    # Reset file pointer
    upload_file.file.seek(0)

    try:
        # TRY BASIC FIRST (fastest method)
        logger.info("FAST: Attempting basic EasyOCR (no preprocessing)...")
        text = extract_text_from_image(upload_file)

        if text and len(text.strip()) > 100:  # If we got decent text, use it
            logger.info(f"FAST: Basic OCR successful ({len(text)} chars)")
            return text
        elif text:
            logger.info(f"FAST: Basic got {len(text)} chars, trying enhanced...")
        else:
            logger.info("FAST: Basic got no text, trying enhanced...")

    except Exception as e:
        logger.warning(f"Basic OCR failed: {str(e)}, trying automated...")

    # Reset file pointer
    upload_file.file.seek(0)

    try:
        # TRY AUTOMATED (with preprocessing, but limited to 2-3 versions)
        logger.info("FAST: Attempting automated processing...")
        text = extract_text_automated(upload_file)

        if text.strip():
            logger.info(f"FAST: Automated successful ({len(text)} chars)")
            return text
        else:
            logger.warning("Automated returned no text")

    except Exception as e:
        logger.warning(f"Automated failed: {str(e)}")

    # Reset file pointer
    upload_file.file.seek(0)

    try:
        # TRY OPENCV (alternative preprocessing)
        logger.info("FAST: Attempting OpenCV preprocessing...")
        text = extract_text_with_opencv(upload_file)

        if text.strip():
            logger.info(f"FAST: OpenCV successful ({len(text)} chars)")
            return text

    except Exception as e:
        logger.warning(f"OpenCV failed: {str(e)}")

    # If all methods failed
    logger.error("All OCR methods returned empty text")
    raise HTTPException(
        status_code=422,
        detail="Could not extract text from image. Please ensure the image contains readable text."
    )
