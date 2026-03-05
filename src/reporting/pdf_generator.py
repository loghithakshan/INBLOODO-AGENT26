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
        
        try:
            from fpdf import FPDF
            
            # Create PDF with explicit margins
            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_page()
            
            # Set larger margins to avoid text overflow  
            pdf.set_left_margin(20)
            pdf.set_top_margin(15)
            pdf.set_right_margin(20)
            
            # Title (smaller font)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "BLOOD ANALYSIS REPORT", 0, 1, "C")
            
            # Timestamp
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, 5, "Analysis Report", 0, 1, "L")
            pdf.ln(2)
            
            # Extracted Parameters Section
            params = analysis_report.get("extracted_parameters", {})
            if params:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 5, "Blood Parameters", 0, 1)
                pdf.set_font("Helvetica", "", 9)
                
                for param_name, param_value in list(params.items())[:8]:
                    # Simplify text to avoid wrapping issues
                    try:
                        text = f"{param_name}: {param_value}"
                        # Truncate if too long
                        if len(text) > 70:
                            text = text[:67] + "..."
                        text = self.sanitize_text(text)
                        pdf.cell(0, 4, text, 0, 1)
                    except:
                        pass
                pdf.ln(1)
            
            # Recommendations Section  
            recommendations = analysis_report.get("recommendations", [])
            if recommendations:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 5, "Recommendations", 0, 1)
                pdf.set_font("Helvetica", "", 8)
                
                for i, rec in enumerate(recommendations[:6], 1):
                    try:
                        text = f"{i}. {rec}"
                        if len(text) > 70:
                            text = text[:67] + "..."
                        text = self.sanitize_text(text)
                        pdf.cell(0, 3, text, 0, 1)
                    except:
                        pass
                pdf.ln(1)
            
            # Analysis Summary
            analysis_count = len(recommendations)
            interpretations = analysis_report.get("interpretations", [])
            interp_count = len(interpretations)
            
            pdf.set_font("Helvetica", "", 8)
            summary = f"Analysis Report: {analysis_count} recommendations, {interp_count} interpretation(s)"
            pdf.cell(0, 5, self.sanitize_text(summary), 0, 1)
            
            # Save PDF
            os.makedirs("reports", exist_ok=True)
            filepath = os.path.join("reports", filename)
            pdf.output(filepath)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"PDF generation error: {str(e)}")
