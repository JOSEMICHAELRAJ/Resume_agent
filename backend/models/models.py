"""
models.py - SQLAlchemy Database Models
Defines all database tables for the Resume Screening System
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Recruiter(db.Model):
    """Recruiter user model"""
    __tablename__ = 'recruiters'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_descriptions = db.relationship('JobDescription', backref='recruiter', lazy=True, cascade='all, delete-orphan')
    rankings = db.relationship('Ranking', backref='recruiter', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Recruiter {self.username}>"


class Candidate(db.Model):
    """Candidate model"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = db.relationship('Resume', backref='candidate', lazy=True, cascade='all, delete-orphan')
    rankings = db.relationship('Ranking', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Candidate {self.full_name}>"


class Resume(db.Model):
    """Resume document model"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, docx, etc.
    raw_text = db.Column(db.LongText, nullable=True)
    
    # Extracted Information
    skills = db.Column(db.JSON, nullable=True)  # List of skills
    experience = db.Column(db.JSON, nullable=True)  # Work experience data
    education = db.Column(db.JSON, nullable=True)  # Education data
    certifications = db.Column(db.JSON, nullable=True)  # Certifications
    
    # Embeddings for semantic search
    text_embedding = db.Column(db.JSON, nullable=True)
    
    is_processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Resume {self.filename}>"


class JobDescription(db.Model):
    """Job description model"""
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    description = db.Column(db.LongText, nullable=False)
    
    # Extracted Information
    required_skills = db.Column(db.JSON, nullable=True)  # List of required skills
    requirements = db.Column(db.JSON, nullable=True)  # Other requirements
    nice_to_have = db.Column(db.JSON, nullable=True)  # Nice to have skills
    
    # Embeddings for semantic search
    text_embedding = db.Column(db.JSON, nullable=True)
    
    is_processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rankings = db.relationship('Ranking', backref='job_description', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<JobDescription {self.title} at {self.company}>"


class Ranking(db.Model):
    """Candidate ranking with job description model"""
    __tablename__ = 'rankings'
    
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False, index=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False, index=True)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    
    # Scoring
    overall_score = db.Column(db.Float, default=0.0)
    skill_match_score = db.Column(db.Float, default=0.0)
    experience_match_score = db.Column(db.Float, default=0.0)
    education_match_score = db.Column(db.Float, default=0.0)
    semantic_similarity_score = db.Column(db.Float, default=0.0)
    
    # Matched Information
    matched_skills = db.Column(db.JSON, nullable=True)
    missing_skills = db.Column(db.JSON, nullable=True)
    experience_years = db.Column(db.Float, nullable=True)
    
    # Generated Insights
    summary = db.Column(db.Text, nullable=True)
    interview_questions = db.Column(db.JSON, nullable=True)  # Generated interview questions
    recommendation = db.Column(db.String(50), default='PENDING')  # SHORTLIST, REJECT, PENDING
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('candidate_id', 'job_description_id', name='unique_candidate_job'),
    )
    
    def __repr__(self):
        return f"<Ranking {self.candidate_id} for Job {self.job_description_id}>"
