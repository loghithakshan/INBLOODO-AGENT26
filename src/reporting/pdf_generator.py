from fpdf import FPDF
import os
from datetime import datetime
import re
import unicodedata

class PDFReportGenerator:
    """Generates a professional PDF report from analysis data."""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Remove or replace Unicode characters that FPDF's default fonts don't support.
        This handles emojis, special symbols, and other non-Latin characters.
        """
        if not text:
            return ""
        
        sanitized = ""
        for char in text:
            try:
                char.encode('latin-1')
                sanitized += char
            except UnicodeEncodeError:
                try:
                    decomposed = unicodedata.normalize('NFKD', char)
                    normalized = decomposed.encode('ASCII', 'ignore').decode('ASCII')
                    if normalized:
                        sanitized += normalized
                    else:
                        if unicodedata.category(char).startswith('S'):
                            sanitized += '*'
                        elif unicodedata.category(char).startswith('P'):
                            sanitized += ' '
                        else:
                            sanitized += ' '
                except:
                    sanitized += ' '
        
        return sanitized.strip()

    def generate_pdf_report(self, analysis_report: dict, filename: str = "report.pdf") -> str:
        """Generate a comprehensive PDF report from analysis data."""
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, self.sanitize_text(analysis_report.get("title", "Blood Report")), ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 12)
        pdf.ln(10)
        
        # Parameters
        if "parameters" in analysis_report:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "Blood Parameters", ln=True)
            pdf.set_font("Helvetica", "", 10)
            
            for param in analysis_report.get("parameters", []):
                text = f"{param.get('name', '')}: {param.get('value', '')} {param.get('unit', '')}"
                pdf.cell(0, 8, self.sanitize_text(text), ln=True)
        
        # Interpretations
        if "interpretations" in analysis_report and analysis_report["interpretations"]:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "Interpretations", ln=True)
            pdf.set_font("Helvetica", "", 10)
            
            for interp in analysis_report.get("interpretations", []):
                sanitized_interp = self.sanitize_text(interp)
                pdf.multi_cell(0, 5, sanitized_interp)
        
        # Risk Assessment
        if "risks" in analysis_report and analysis_report["risks"]:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "Risk Assessment", ln=True)
            pdf.set_font("Helvetica", "", 10)
            
            for risk in analysis_report.get("risks", []):
                sanitized_risk = self.sanitize_text(risk)
                pdf.multi_cell(0, 5, sanitized_risk)
        
        # Recommendations
        if "recommendations" in analysis_report and analysis_report["recommendations"]:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, "Recommendations", ln=True)
            pdf.set_font("Helvetica", "", 10)
            
            for rec in analysis_report.get("recommendations", []):
                sanitized_rec = self.sanitize_text(rec)
                pdf.multi_cell(0, 5, f"- {sanitized_rec}")
        
        # Save PDF
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        pdf.output(filepath)
        
        return filepath
