"""
ai_agent.py - AI Agent Module
Uses LangChain and OpenAI to generate insights and recommendations
"""

import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.logger import app_logger


class ResumeAIAgent:
    """
    AI Agent for generating insights, summaries, and recommendations
    """
    
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        """
        Initialize the AI Agent
        
        Args:
            api_key: OpenAI API key
            model: Model name
        """
        try:
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.model = model
            self.llm = OpenAI(
                openai_api_key=self.api_key,
                model_name=model,
                temperature=0.7,
                max_tokens=500
            )
            app_logger.info(f"Initialized AI Agent with model: {model}")
        except Exception as e:
            app_logger.error(f"Error initializing AI Agent: {str(e)}")
            self.llm = None
    
    def generate_candidate_summary(self, resume_text, job_description):
        """
        Generate a summary of candidate fit for the job
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description
        
        Returns:
            Summary text
        """
        if not self.llm:
            return "AI Agent not initialized"
        
        try:
            # Truncate texts to reasonable length
            resume_text = resume_text[:2000]
            job_description = job_description[:1000]
            
            prompt_template = PromptTemplate(
                input_variables=["resume", "job_description"],
                template="""Based on the following resume and job description, provide a brief summary (2-3 sentences) of how well the candidate fits the role:

Resume:
{resume}

Job Description:
{job_description}

Summary:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            summary = chain.run(resume=resume_text, job_description=job_description)
            
            app_logger.info("Generated candidate summary")
            return summary.strip()
        
        except Exception as e:
            app_logger.error(f"Error generating candidate summary: {str(e)}")
            return "Unable to generate summary"
    
    def generate_interview_questions(self, resume_text, missing_skills, job_title):
        """
        Generate interview questions based on resume and missing skills
        
        Args:
            resume_text: Extracted resume text
            missing_skills: List of skills not found in resume
            job_title: Job title
        
        Returns:
            List of interview questions
        """
        if not self.llm:
            return []
        
        try:
            # Prepare missing skills text
            missing_skills_text = ", ".join(missing_skills[:5]) if missing_skills else "N/A"
            resume_text = resume_text[:1500]
            
            prompt_template = PromptTemplate(
                input_variables=["resume", "missing_skills", "job_title"],
                template="""Generate 3-4 specific interview questions for a {job_title} candidate based on:
1. Their resume: {resume}
2. Missing skills they need to develop: {missing_skills}

Format as a numbered list:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            response = chain.run(
                resume=resume_text,
                missing_skills=missing_skills_text,
                job_title=job_title
            )
            
            # Parse response into list of questions
            questions = [q.strip() for q in response.split('\n') if q.strip()]
            
            app_logger.info(f"Generated {len(questions)} interview questions")
            return questions[:5]  # Return top 5 questions
        
        except Exception as e:
            app_logger.error(f"Error generating interview questions: {str(e)}")
            return []
    
    def generate_improvement_suggestions(self, missing_skills, experience_gap):
        """
        Generate suggestions for candidate improvement
        
        Args:
            missing_skills: List of missing skills
            experience_gap: Experience gap (years)
        
        Returns:
            Improvement suggestions
        """
        if not self.llm:
            return "AI Agent not initialized"
        
        try:
            missing_skills_text = ", ".join(missing_skills[:10]) if missing_skills else "None"
            
            prompt_template = PromptTemplate(
                input_variables=["missing_skills", "experience_gap"],
                template="""Provide 3-4 specific suggestions for a candidate to improve their qualifications for this role:
Missing skills: {missing_skills}
Experience gap: {experience_gap} years

Suggestions:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            suggestions = chain.run(
                missing_skills=missing_skills_text,
                experience_gap=str(experience_gap)
            )
            
            app_logger.info("Generated improvement suggestions")
            return suggestions.strip()
        
        except Exception as e:
            app_logger.error(f"Error generating suggestions: {str(e)}")
            return "Unable to generate suggestions"


# For cases where OpenAI is not available, use fallback implementations
class FallbackAIAgent:
    """
    Fallback AI Agent with template-based responses
    """
    
    @staticmethod
    def generate_candidate_summary(resume_text, job_description):
        """Generate template-based summary"""
        return "Candidate has relevant experience and skills that align with the job requirements."
    
    @staticmethod
    def generate_interview_questions(resume_text, missing_skills, job_title):
        """Generate template-based interview questions"""
        questions = [
            f"Tell us about your experience with {missing_skills[0] if missing_skills else 'your primary skills'}.",
            f"How do you approach learning new technologies relevant to a {job_title} role?",
            "Describe a challenging problem you solved in your previous role.",
            "What are your career goals and how does this position align with them?"
        ]
        return questions[:4]
    
    @staticmethod
    def generate_improvement_suggestions(missing_skills, experience_gap):
        """Generate template-based improvement suggestions"""
        return f"1. Develop skills in {missing_skills[0] if missing_skills else 'the required technologies'}\n2. Gain additional {experience_gap} years of experience\n3. Complete relevant certifications"
