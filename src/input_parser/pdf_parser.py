import fitz  # PyMuPDF
import tempfile
import os
from fastapi import UploadFile
import numpy as np
import io
from PIL import Image
from src.input_parser.image_parser import get_reader
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(upload_file: UploadFile) -> str:
    """
    Extract text from an uploaded PDF file (FastAPI UploadFile).
    Optimized: skips OCR if text layer exists, downscales OCR images.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = tmp.name

    try:
        doc = fitz.open(tmp_path)
        text_parts = []
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(page_text)
            else:
                # No text layer — OCR the page image
                ocr_reader = get_reader()
                if ocr_reader:
                    # Use lower DPI for speed (default is 72, we use 150 instead of 300)
                    pix = page.get_pixmap(dpi=150)
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Downscale large pages for faster OCR
                    max_size = 1000
                    if max(img.size) > max_size:
                        ratio = max_size / max(img.size)
                        new_size = tuple(int(d * ratio) for d in img.size)
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    img_np = np.array(img)
                    results = ocr_reader.readtext(img_np, detail=0, batch_size=4, paragraph=True)
                    page_text = ' '.join(results)
                    text_parts.append(page_text)
                    del img, img_np  # Free memory
                    
                    logger.info(f"OCR'd page {page_num + 1}: {len(page_text)} chars")
                
        doc.close()
        return '\n'.join(text_parts)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
