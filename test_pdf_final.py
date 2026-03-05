import sys
import os
sys.path.insert(0, "c:\\Users\\rakes\\Downloads\\blood report ai")

from src.reporting.pdf_generator import PDFReportGenerator
from src.agent.agent_orchestrator import MultiAgentOrchestrator
import asyncio

async def test_pdf_generation():
    print("=== Testing PDF Generation ===\n")
    
    # 1. First, generate analysis
    print("1. Generating analysis...")
    orchestrator = MultiAgentOrchestrator()
    params = {
        "hemoglobin": 13.5,
        "glucose": 95,
        "cholesterol": 185,
        "ldl": 110,
        "hdl": 50,
        "triglycerides": 120,
        "creatinine": 0.9,
        "potassium": 4.2
    }
    
    report = await orchestrator.execute(params)
    print(f"    Analysis completed: {report.status}")
    
    # 2. Generate PDF
    print("\n2. Generating PDF report...")
    pdf_gen = PDFReportGenerator()
    
    # Convert report to dict for PDF generation
    report_dict = {
        "extracted_parameters": report.extracted_parameters,
        "interpretations": report.interpretations,
        "risks": report.risks,
        "recommendations": report.recommendations,
        "prescriptions": report.prescriptions,
        "synthesis": report.synthesis,
        "timestamp": report.timestamp
    }
    
    try:
        pdf_path = pdf_gen.generate_pdf_report(report_dict, "test_analysis_report.pdf")
        print(f"    PDF generated: {pdf_path}")
        
        # Check if file exists
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"    File size: {file_size:,} bytes")
        else:
            print("    PDF file not found!")
            
    except Exception as e:
        print(f"    PDF generation failed: {str(e)}")

# Run async test
asyncio.run(test_pdf_generation())
