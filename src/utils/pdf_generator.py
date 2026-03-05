"""
PDF Report Generation Module
Generates professional PDF reports from blood analysis results.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io
import logging

logger = logging.getLogger(__name__)


def generate_pdf_report(analysis_result: dict, filename: str = None) -> bytes:
    """
    Generate a professional PDF report from blood analysis results.
    
    Args:
        analysis_result: Dictionary containing analysis data with keys:
            - extracted_parameters: dict of blood parameters
            - interpretations: list of interpretations
            - risks: list of identified risks
            - recommendations: list of health recommendations
            - prescriptions: list of prescriptions/treatments
        filename: Optional output filename
    
    Returns:
        PDF content as bytes
    """
    try:
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=10,
            spaceBefore=10
        )
        
        # Title
        story.append(Paragraph("Blood Report Analysis", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Parameters Section
        if analysis_result.get('extracted_parameters'):
            story.append(Paragraph("Extracted Parameters", heading_style))
            params = analysis_result['extracted_parameters']
            param_data = [['Parameter', 'Value', 'Unit']]
            
            # Common units for blood parameters
            units = {
                'hemoglobin': 'g/dL',
                'glucose': 'mg/dL',
                'cholesterol': 'mg/dL',
                'triglycerides': 'mg/dL',
                'hdl': 'mg/dL',
                'ldl': 'mg/dL',
                'creatinine': 'mg/dL',
                'urea': 'mg/dL',
                'bilirubin': 'mg/dL',
                'alt': 'U/L',
                'ast': 'U/L',
                'alp': 'U/L',
                'sodium': 'mEq/L',
                'potassium': 'mEq/L',
                'calcium': 'mg/dL',
            }
            
            for param, value in params.items():
                unit = units.get(param.lower(), '')
                param_data.append([
                    param.replace('_', ' ').title(),
                    f"{value:.2f}" if isinstance(value, (int, float)) else str(value),
                    unit
                ])
            
            param_table = Table(param_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            param_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(param_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Interpretations Section
        if analysis_result.get('interpretations'):
            story.append(Paragraph("Parameter Interpretations", heading_style))
            for interpretation in analysis_result['interpretations'][:5]:
                if isinstance(interpretation, dict):
                    param = interpretation.get('parameter', 'Value')
                    status = interpretation.get('status', 'Unknown').upper()
                    interp = interpretation.get('interpretation', '')
                    story.append(Paragraph(f"<b>{param}:</b> {status} - {interp}", styles['Normal']))
                else:
                    story.append(Paragraph(str(interpretation), styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Risks Section
        if analysis_result.get('risks'):
            story.append(Paragraph("Identified Health Risks", heading_style))
            for risk in analysis_result['risks'][:5]:
                if isinstance(risk, dict):
                    category = risk.get('category', 'Health').title()
                    severity = risk.get('severity', 'unknown').upper()
                    description = risk.get('description', '')
                    story.append(Paragraph(f"<b>{category} ({severity}):</b> {description}", styles['Normal']))
                else:
                    story.append(Paragraph(str(risk), styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Recommendations Section
        if analysis_result.get('recommendations'):
            story.append(Paragraph("Health Recommendations", heading_style))
            for i, rec in enumerate(analysis_result['recommendations'][:8], 1):
                if isinstance(rec, dict):
                    text = rec.get('recommendation', str(rec))
                else:
                    text = str(rec)
                story.append(Paragraph(f"<b>{i}.</b> {text}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Prescriptions Section
        if analysis_result.get('prescriptions'):
            story.append(Paragraph("Medical Guidance", heading_style))
            for prescription in analysis_result['prescriptions'][:5]:
                if isinstance(prescription, dict):
                    text = prescription.get('prescription', str(prescription))
                else:
                    text = str(prescription)
                story.append(Paragraph(f"• {text}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise


def save_pdf_report(analysis_result: dict, output_path: str) -> str:
    """
    Save PDF report to file.
    
    Args:
        analysis_result: Analysis result dictionary
        output_path: Path to save PDF file
    
    Returns:
        Path to saved PDF file
    """
    try:
        pdf_content = generate_pdf_report(analysis_result)
        with open(output_path, 'wb') as f:
            f.write(pdf_content)
        logger.info(f"PDF report saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error saving PDF: {str(e)}")
        raise
