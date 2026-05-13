"""
matcher.py - AI Matching Engine
Semantic similarity matching between resumes and job descriptions
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.logger import app_logger


class SemanticMatcher:
    """
    Performs semantic similarity matching between resumes and job descriptions
    Uses sentence transformers for embedding generation
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the semantic matcher
        
        Args:
            model_name: Name of the sentence transformer model
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            app_logger.info(f"Initialized SemanticMatcher with model: {model_name}")
        except Exception as e:
            app_logger.error(f"Error initializing SemanticMatcher: {str(e)}")
            raise
    
    def generate_embedding(self, text):
        """
        Generate embedding for text
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            app_logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0-1)
        """
        try:
            embedding1 = self.generate_embedding(text1)
            embedding2 = self.generate_embedding(text2)
            
            similarity = cosine_similarity(
                [embedding1],
                [embedding2]
            )[0][0]
            
            return float(similarity)
        except Exception as e:
            app_logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def batch_similarity(self, texts1, texts2):
        """
        Calculate similarity between multiple text pairs
        
        Args:
            texts1: List of texts
            texts2: List of texts
        
        Returns:
            Similarity matrix
        """
        try:
            embeddings1 = self.model.encode(texts1, convert_to_numpy=True)
            embeddings2 = self.model.encode(texts2, convert_to_numpy=True)
            
            similarities = cosine_similarity(embeddings1, embeddings2)
            return similarities
        except Exception as e:
            app_logger.error(f"Error calculating batch similarity: {str(e)}")
            raise


class SkillMatcher:
    """
    Matches skills between resume and job description
    """
    
    def __init__(self):
        """Initialize skill matcher"""
        self.matcher = SemanticMatcher()
    
    def match_skills(self, resume_skills, jd_skills):
        """
        Match skills between resume and job description
        
        Args:
            resume_skills: Dictionary of resume skills
            jd_skills: List of required skills from JD
        
        Returns:
            Dictionary with matched and missing skills
        """
        try:
            # Flatten resume skills
            resume_skills_flat = []
            if isinstance(resume_skills, dict):
                for category, skills in resume_skills.items():
                    if isinstance(skills, list):
                        resume_skills_flat.extend(skills)
            else:
                resume_skills_flat = resume_skills if isinstance(resume_skills, list) else []
            
            matched_skills = []
            missing_skills = []
            
            for jd_skill in jd_skills:
                # Direct match
                if jd_skill.lower() in [s.lower() for s in resume_skills_flat]:
                    matched_skills.append(jd_skill)
                else:
                    # Semantic similarity match
                    best_match_score = 0
                    best_match_skill = None
                    
                    for resume_skill in resume_skills_flat:
                        score = self.matcher.calculate_similarity(jd_skill, resume_skill)
                        if score > best_match_score:
                            best_match_score = score
                            best_match_skill = resume_skill
                    
                    if best_match_score > 0.7:  # Threshold for semantic match
                        matched_skills.append(jd_skill)
                    else:
                        missing_skills.append(jd_skill)
            
            app_logger.info(f"Skill matching complete: {len(matched_skills)} matched, {len(missing_skills)} missing")
            
            return {
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'match_percentage': (len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0
            }
        
        except Exception as e:
            app_logger.error(f"Error in skill matching: {str(e)}")
            return {
                'matched_skills': [],
                'missing_skills': jd_skills,
                'match_percentage': 0
            }
    
    def extract_skills_from_text(self, text, keywords=None):
        """
        Extract skills from text using keyword matching
        
        Args:
            text: Resume or JD text
            keywords: List of skill keywords to look for
        
        Returns:
            List of found skills
        """
        skills = []
        text_lower = text.lower()
        
        for keyword in (keywords or []):
            if keyword.lower() in text_lower:
                skills.append(keyword)
        
        return skills


class ExperienceMatcher:
    """
    Matches experience requirements between resume and job description
    """
    
    @staticmethod
    def match_experience(resume_experience, required_years):
        """
        Match experience requirements
        
        Args:
            resume_experience: Years of experience from resume
            required_years: Required years from job description
        
        Returns:
            Dictionary with experience match info
        """
        try:
            resume_years = resume_experience.get('total_years', 0)
            match_score = 0
            recommendation = "NO_MATCH"
            
            if resume_years >= required_years:
                match_score = min(100, 100 * (resume_years / required_years))
                recommendation = "MATCH"
            elif resume_years >= (required_years * 0.8):
                match_score = 80
                recommendation = "PARTIAL_MATCH"
            else:
                match_score = max(0, (resume_years / required_years) * 100)
                recommendation = "NO_MATCH"
            
            return {
                'resume_years': resume_years,
                'required_years': required_years,
                'match_score': match_score,
                'recommendation': recommendation
            }
        
        except Exception as e:
            app_logger.error(f"Error matching experience: {str(e)}")
            return {
                'resume_years': 0,
                'required_years': required_years,
                'match_score': 0,
                'recommendation': "ERROR"
            }
