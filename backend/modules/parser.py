"""
parser.py - Resume Parser Module
Extracts text and structured information from resume files
"""

import PyPDF2
import pdfplumber
from docx import Document
import re
import json
from utils.logger import app_logger


class ResumeParser:
    """
    Parser for extracting text and information from resumes
    Supports PDF and DOCX formats
    """
    
    def __init__(self):
        self.skills_keywords = self._load_skills_keywords()
        self.certifications_pattern = self._load_certifications_pattern()
    
    def _load_skills_keywords(self):
        """Load common technical skills for extraction"""
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'csharp', 'c++',
                'golang', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala',
                'r', 'matlab', 'perl', 'groovy'
            ],
            'web_frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'nodejs',
                'express', 'laravel', 'rails', 'asp.net', 'fastapi'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
                'elasticsearch', 'dynamodb', 'oracle', 'sqlserver', 'mariadb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean'
            ],
            'devops': [
                'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'ci/cd',
                'ansible', 'terraform', 'cloudformation'
            ],
            'tools': [
                'git', 'jira', 'confluence', 'slack', 'figma', 'postman'
            ]
        }
    
    def _load_certifications_pattern(self):
        """Load certification patterns for extraction"""
        return [
            'AWS Certified', 'Azure Certified', 'GCP Certified',
            'PMP', 'CISP', 'CCNA', 'OSCP',
            'Certified', 'Certification'
        ]
    
    def extract_text_from_pdf(self, file_path):
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            Extracted text string
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
            
            app_logger.info(f"Successfully extracted text from PDF: {file_path}")
            return text
        except Exception as e:
            app_logger.error(f"Error extracting PDF: {str(e)}")
            raise
    
    def extract_text_from_docx(self, file_path):
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
        
        Returns:
            Extracted text string
        """
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            app_logger.info(f"Successfully extracted text from DOCX: {file_path}")
            return text
        except Exception as e:
            app_logger.error(f"Error extracting DOCX: {str(e)}")
            raise
    
    def extract_text_from_file(self, file_path):
        """
        Extract text from file (PDF or DOCX)
        
        Args:
            file_path: Path to file
        
        Returns:
            Extracted text string
        """
        file_extension = file_path.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_skills(self, text):
        """
        Extract skills from resume text
        
        Args:
            text: Resume text
        
        Returns:
            Dictionary of extracted skills
        """
        text_lower = text.lower()
        extracted_skills = {}
        
        for category, keywords in self.skills_keywords.items():
            found_skills = []
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills.append(keyword)
            if found_skills:
                extracted_skills[category] = list(set(found_skills))
        
        return extracted_skills
    
    def extract_experience(self, text):
        """
        Extract work experience from resume text
        
        Args:
            text: Resume text
        
        Returns:
            Dictionary of extracted experience
        """
        # Simple pattern for years of experience
        experience_pattern = r'(\d+)\+?\s+(?:years?|yrs?) of experience'
        matches = re.findall(experience_pattern, text, re.IGNORECASE)
        
        experience_data = {
            'total_years': float(matches[0]) if matches else 0,
            'roles_count': len(re.findall(r'(?:worked|employed|managed|led|developed)', text, re.IGNORECASE))
        }
        
        return experience_data
    
    def extract_education(self, text):
        """
        Extract education information from resume
        
        Args:
            text: Resume text
        
        Returns:
            List of education entries
        """
        education_keywords = ['bachelor', 'master', 'phd', 'diploma', 'b.s.', 'm.s.', 'b.a.', 'm.a.']
        education_entries = []
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in education_keywords):
                education_entries.append(line.strip())
        
        return education_entries[:5]  # Return top 5 education entries
    
    def extract_certifications(self, text):
        """
        Extract certifications from resume
        
        Args:
            text: Resume text
        
        Returns:
            List of certifications
        """
        certifications = []
        
        for pattern in self.certifications_pattern:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context around match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                certifications.append(context)
        
        return list(set(certifications))[:10]  # Return unique certifications
    
    def extract_contact_info(self, text):
        """
        Extract contact information from resume
        
        Args:
            text: Resume text
        
        Returns:
            Dictionary of contact information
        """
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        return contact_info
    
    def parse_resume(self, file_path):
        """
        Complete resume parsing
        
        Args:
            file_path: Path to resume file
        
        Returns:
            Dictionary containing all extracted information
        """
        try:
            # Extract raw text
            raw_text = self.extract_text_from_file(file_path)
            
            # Extract structured information
            parsed_data = {
                'raw_text': raw_text,
                'skills': self.extract_skills(raw_text),
                'experience': self.extract_experience(raw_text),
                'education': self.extract_education(raw_text),
                'certifications': self.extract_certifications(raw_text),
                'contact_info': self.extract_contact_info(raw_text)
            }
            
            app_logger.info(f"Successfully parsed resume: {file_path}")
            return parsed_data
        
        except Exception as e:
            app_logger.error(f"Error parsing resume: {str(e)}")
            raise
