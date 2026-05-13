"""
database.py - Database Utility Functions
Handles database initialization and common operations
"""

from models.models import db, Recruiter, Candidate, Resume, JobDescription, Ranking
from utils.logger import app_logger
from datetime import datetime


class DatabaseManager:
    """
    Manages database operations
    """
    
    @staticmethod
    def init_db(app):
        """
        Initialize database tables
        
        Args:
            app: Flask application instance
        """
        try:
            with app.app_context():
                db.create_all()
                app_logger.info("Database initialized successfully")
        except Exception as e:
            app_logger.error(f"Error initializing database: {str(e)}")
            raise
    
    @staticmethod
    def create_recruiter(username, email, password_hash, full_name, company=None, department=None):
        """
        Create a new recruiter
        
        Args:
            username: Username
            email: Email address
            password_hash: Hashed password
            full_name: Full name
            company: Company name
            department: Department
        
        Returns:
            Recruiter object
        """
        try:
            recruiter = Recruiter(
                username=username,
                email=email,
                password_hash=password_hash,
                full_name=full_name,
                company=company,
                department=department
            )
            db.session.add(recruiter)
            db.session.commit()
            app_logger.info(f"Recruiter created: {username}")
            return recruiter
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error creating recruiter: {str(e)}")
            raise
    
    @staticmethod
    def create_candidate(full_name, email=None, phone=None, location=None):
        """
        Create a new candidate
        
        Args:
            full_name: Full name
            email: Email address
            phone: Phone number
            location: Location
        
        Returns:
            Candidate object
        """
        try:
            candidate = Candidate(
                full_name=full_name,
                email=email,
                phone=phone,
                location=location
            )
            db.session.add(candidate)
            db.session.commit()
            app_logger.info(f"Candidate created: {full_name}")
            return candidate
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error creating candidate: {str(e)}")
            raise
    
    @staticmethod
    def create_resume(candidate_id, filename, file_path, file_type, raw_text=None, parsed_data=None):
        """
        Create a new resume record
        
        Args:
            candidate_id: Candidate ID
            filename: Original filename
            file_path: Path to stored file
            file_type: File type (pdf, docx)
            raw_text: Extracted raw text
            parsed_data: Dictionary with parsed information
        
        Returns:
            Resume object
        """
        try:
            resume = Resume(
                candidate_id=candidate_id,
                filename=filename,
                file_path=file_path,
                file_type=file_type,
                raw_text=raw_text,
                skills=parsed_data.get('skills') if parsed_data else None,
                experience=parsed_data.get('experience') if parsed_data else None,
                education=parsed_data.get('education') if parsed_data else None,
                certifications=parsed_data.get('certifications') if parsed_data else None,
                is_processed=True
            )
            db.session.add(resume)
            db.session.commit()
            app_logger.info(f"Resume created for candidate {candidate_id}: {filename}")
            return resume
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error creating resume: {str(e)}")
            raise
    
    @staticmethod
    def create_job_description(recruiter_id, title, company, description, extracted_data=None):
        """
        Create a new job description
        
        Args:
            recruiter_id: Recruiter ID
            title: Job title
            company: Company name
            description: Job description text
            extracted_data: Dictionary with extracted information
        
        Returns:
            JobDescription object
        """
        try:
            job_desc = JobDescription(
                recruiter_id=recruiter_id,
                title=title,
                company=company,
                description=description,
                required_skills=extracted_data.get('required_skills') if extracted_data else None,
                requirements=extracted_data.get('requirements') if extracted_data else None,
                nice_to_have=extracted_data.get('nice_to_have') if extracted_data else None,
                is_processed=True
            )
            db.session.add(job_desc)
            db.session.commit()
            app_logger.info(f"Job description created: {title}")
            return job_desc
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error creating job description: {str(e)}")
            raise
    
    @staticmethod
    def create_ranking(recruiter_id, candidate_id, job_description_id, resume_id=None, scores=None):
        """
        Create or update a ranking record
        
        Args:
            recruiter_id: Recruiter ID
            candidate_id: Candidate ID
            job_description_id: Job Description ID
            resume_id: Resume ID (optional)
            scores: Dictionary with scoring information
        
        Returns:
            Ranking object
        """
        try:
            ranking = Ranking.query.filter_by(
                candidate_id=candidate_id,
                job_description_id=job_description_id
            ).first()
            
            if not ranking:
                ranking = Ranking(
                    recruiter_id=recruiter_id,
                    candidate_id=candidate_id,
                    job_description_id=job_description_id,
                    resume_id=resume_id
                )
            
            if scores:
                ranking.overall_score = scores.get('overall_score', 0)
                ranking.skill_match_score = scores.get('skill_match_score', 0)
                ranking.experience_match_score = scores.get('experience_match_score', 0)
                ranking.education_match_score = scores.get('education_match_score', 0)
                ranking.semantic_similarity_score = scores.get('semantic_similarity_score', 0)
                ranking.matched_skills = scores.get('matched_skills', [])
                ranking.missing_skills = scores.get('missing_skills', [])
                ranking.summary = scores.get('summary')
                ranking.interview_questions = scores.get('interview_questions', [])
                ranking.recommendation = scores.get('recommendation', 'PENDING')
                ranking.experience_years = scores.get('experience_years', 0)
            
            db.session.add(ranking)
            db.session.commit()
            app_logger.info(f"Ranking created/updated for candidate {candidate_id}")
            return ranking
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error creating ranking: {str(e)}")
            raise
    
    @staticmethod
    def get_candidate_rankings(job_description_id, limit=None):
        """
        Get rankings for a job description
        
        Args:
            job_description_id: Job Description ID
            limit: Maximum number of results
        
        Returns:
            List of rankings
        """
        try:
            query = Ranking.query.filter_by(
                job_description_id=job_description_id
            ).order_by(Ranking.overall_score.desc())
            
            if limit:
                query = query.limit(limit)
            
            rankings = query.all()
            app_logger.info(f"Retrieved {len(rankings)} rankings for job {job_description_id}")
            return rankings
        except Exception as e:
            app_logger.error(f"Error retrieving rankings: {str(e)}")
            return []
    
    @staticmethod
    def search_candidates(keyword, limit=10):
        """
        Search candidates by name or email
        
        Args:
            keyword: Search keyword
            limit: Maximum number of results
        
        Returns:
            List of candidates
        """
        try:
            candidates = Candidate.query.filter(
                (Candidate.full_name.ilike(f"%{keyword}%")) |
                (Candidate.email.ilike(f"%{keyword}%"))
            ).limit(limit).all()
            
            app_logger.info(f"Found {len(candidates)} candidates matching '{keyword}'")
            return candidates
        except Exception as e:
            app_logger.error(f"Error searching candidates: {str(e)}")
            return []
    
    @staticmethod
    def get_recruiter_jobs(recruiter_id, limit=None):
        """
        Get jobs posted by a recruiter
        
        Args:
            recruiter_id: Recruiter ID
            limit: Maximum number of results
        
        Returns:
            List of job descriptions
        """
        try:
            query = JobDescription.query.filter_by(recruiter_id=recruiter_id).order_by(
                JobDescription.created_at.desc()
            )
            
            if limit:
                query = query.limit(limit)
            
            jobs = query.all()
            app_logger.info(f"Retrieved {len(jobs)} jobs for recruiter {recruiter_id}")
            return jobs
        except Exception as e:
            app_logger.error(f"Error retrieving recruiter jobs: {str(e)}")
            return []
