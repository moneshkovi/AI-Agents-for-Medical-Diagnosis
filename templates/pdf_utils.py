"""
PDF Generation utilities for the AI Medical Diagnosis System
"""

import os
import re
import uuid
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


class PDFReport:
    """Generate PDF reports from medical diagnosis data"""
    
    def __init__(self, output_dir: str = "Results"):
        """Initialize the PDF report generator
        
        Args:
            output_dir: Directory to save PDF reports
        """
        self.output_dir = output_dir
        self.template_dir = os.path.dirname(os.path.abspath(__file__))
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.css_path = os.path.join(self.template_dir, "clinical_style.css")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def _load_css(self) -> str:
        """Load CSS content from file
        
        Returns:
            str: CSS content
        """
        with open(self.css_path, 'r') as f:
            return f.read()
    
    def _extract_patient_info(self, medical_report: str) -> Dict[str, str]:
        """Extract patient information from medical report
        
        Args:
            medical_report: Raw medical report text
            
        Returns:
            dict: Extracted patient information
        """
        # Default values
        patient_info = {
            "name": "Unknown",
            "age": "Unknown",
            "gender": "Unknown",
            "report_date": datetime.datetime.now().strftime("%B %d, %Y")
        }
        
        # Try to extract name
        name_match = re.search(r"(?:Patient|Name):\s*([A-Za-z\s]+)", medical_report)
        if name_match:
            patient_info["name"] = name_match.group(1).strip()
        
        # Try to extract age
        age_match = re.search(r"Age:\s*(\d+)", medical_report)
        if age_match:
            patient_info["age"] = age_match.group(1)
        
        # Try to extract gender
        gender_match = re.search(r"(?:Gender|Sex):\s*([A-Za-z]+)", medical_report)
        if gender_match:
            patient_info["gender"] = gender_match.group(1)
        
        return patient_info
    
    def _format_report_content(self, content: str) -> str:
        """Format report content for HTML display
        
        Args:
            content: Raw report content
            
        Returns:
            str: HTML formatted content
        """
        # Convert plain text to HTML format with proper line breaks
        if content:
            # Convert Markdown headings to HTML headings
            content = re.sub(r'^###\s+(.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
            content = re.sub(r'^##\s+(.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
            
            # Convert Markdown bold to HTML bold
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            
            # Convert Markdown italic to HTML italic
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            
            # Format bullet points as proper HTML list
            bullet_pattern = re.compile(r'^\s*[-•*]\s+(.*?)$', re.MULTILINE)
            if bullet_pattern.search(content):
                # If we have bullet points, wrap them in a list
                lines = content.split('\n')
                formatted_lines = []
                in_list = False
                
                for line in lines:
                    bullet_match = bullet_pattern.match(line)
                    if bullet_match:
                        if not in_list:
                            formatted_lines.append('<ul>')
                            in_list = True
                        formatted_lines.append(f'<li>{bullet_match.group(1)}</li>')
                    else:
                        if in_list:
                            formatted_lines.append('</ul>')
                            in_list = False
                        formatted_lines.append(line)
                
                if in_list:
                    formatted_lines.append('</ul>')
                
                content = '\n'.join(formatted_lines)
            
            # Convert remaining newlines to <br> tags
            content = content.replace('\n\n', '<br><br>')
            content = content.replace('\n', '<br>')
            
            # Clean up any <br> before or after HTML tags
            content = re.sub(r'<br>\s*<(h[0-9]|ul|li|/ul|/li|/h[0-9])>', r'<\1>', content)
            content = re.sub(r'</(h[0-9]|ul|li)>\s*<br>', r'</\1>', content)
            
            # Remove any leading <br>
            content = re.sub(r'^<br>', '', content)
            
            return content
        
        return "<em>No information available</em>"
    
    def generate_pdf(self, 
                    medical_report: str,
                    cardiologist_report: str,
                    psychologist_report: str, 
                    pulmonologist_report: str,
                    final_diagnosis: str,
                    output_filename: Optional[str] = None) -> str:
        """Generate a PDF report from medical diagnosis data
        
        Args:
            medical_report: The original medical report text
            cardiologist_report: Cardiologist's assessment
            psychologist_report: Psychologist's assessment
            pulmonologist_report: Pulmonologist's assessment
            final_diagnosis: Final diagnosis from multidisciplinary team
            output_filename: Optional filename for the PDF; if None, a name will be generated
            
        Returns:
            str: Path to the generated PDF file
        """
        # Extract patient information
        patient_info = self._extract_patient_info(medical_report)
        
        # Format report content for HTML
        formatted_cardiologist = self._format_report_content(cardiologist_report)
        formatted_psychologist = self._format_report_content(psychologist_report)
        formatted_pulmonologist = self._format_report_content(pulmonologist_report)
        formatted_diagnosis = self._format_report_content(final_diagnosis)
        
        # Load CSS
        css_content = self._load_css()
        
        # Generate report ID and timestamp
        report_id = f"MDR-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare template context
        context = {
            "report_id": report_id,
            "timestamp": timestamp,
            "patient_name": patient_info["name"],
            "patient_age": patient_info["age"],
            "patient_gender": patient_info["gender"],
            "report_date": patient_info["report_date"],
            "cardiologist_report": formatted_cardiologist,
            "psychologist_report": formatted_psychologist,
            "pulmonologist_report": formatted_pulmonologist,
            "final_diagnosis": formatted_diagnosis,
            "css_content": css_content,
            "current_year": datetime.datetime.now().year
        }
        
        # Render HTML template
        template = self.env.get_template("base_report.html")
        html_content = template.render(**context)
        
        # Generate filename if not provided
        if not output_filename:
            patient_name_slug = patient_info["name"].lower().replace(" ", "_")
            output_filename = f"medical_report_{patient_name_slug}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Ensure .pdf extension
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        # Generate full output path
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
