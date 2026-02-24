"""
Optimized PDF Processing Engine
Handles concurrent PDF generation with support for all report types.
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from src.reporting.pdf_generator import PDFReportGenerator

logger = logging.getLogger(__name__)

class OptimizedPDFProcessor:
    """Handles fast PDF generation with concurrency."""
    
    def __init__(self, max_workers: int = 3):
        self.pdf_gen = PDFReportGenerator()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.processing_queue = {}
        logger.info(f"OptimizedPDFProcessor initialized with {max_workers} workers")
    
    async def generate_pdf_async(
        self, 
        analysis_data: Dict[str, Any],
        user_id: int,
        report_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate PDF asynchronously without blocking the response."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{user_id}_{report_id or timestamp}.pdf"
            
            loop = asyncio.get_event_loop()
            pdf_path = await loop.run_in_executor(
                self.executor,
                self._generate_pdf_sync,
                analysis_data,
                filename
            )
            
            logger.info(f"PDF generated successfully: {pdf_path}")
            return {
                "status": "success",
                "pdf_path": pdf_path,
                "filename": filename,
                "size_bytes": os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
            }
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "pdf_path": None
            }
    
    def _generate_pdf_sync(self, analysis_data: Dict[str, Any], filename: str) -> str:
        """Synchronous PDF generation runs in thread pool."""
        try:
            return self.pdf_gen.generate_pdf_report(analysis_data, filename)
        except Exception as e:
            logger.error(f"PDF sync generation failed: {str(e)}")
            raise
    
    def cleanup(self):
        """Cleanup thread pool resources."""
        self.executor.shutdown(wait=False)


class PDFProcessingService:
    """Service for handling PDF operations."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.processor = OptimizedPDFProcessor(max_workers=4)
        return cls._instance
    
    async def process_blood_report(
        self,
        analysis_data: Dict[str, Any],
        user_id: int,
        report_id: Optional[int] = None,
        background: bool = True
    ) -> Dict[str, Any]:
        """Process blood report with fast settings."""
        
        logger.info(f"Processing blood report for user {user_id}")
        
        if background:
            asyncio.create_task(
                self.processor.generate_pdf_async(analysis_data, user_id, report_id)
            )
            return {
                "status": "processing",
                "message": "PDF generation started in background",
                "report_id": report_id
            }
        else:
            return await self.processor.generate_pdf_async(
                analysis_data,
                user_id,
                report_id
            )
    
    async def process_medical_report(
        self,
        analysis_data: Dict[str, Any],
        user_id: int,
        report_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Alias for blood report processing."""
        return await self.process_blood_report(
            analysis_data,
            user_id,
            report_id,
            background=True
        )
