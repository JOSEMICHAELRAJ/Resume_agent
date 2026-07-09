"""
job_routes.py - Job Description Routes
"""

from flask import Blueprint, request, jsonify, current_app
from models.models import db, JobDescription, Recruiter, Candidate, Resume
from modules.matcher import SkillMatcher
from utils.logger import app_logger
from utils.database import DatabaseManager

job_bp = Blueprint('job', __name__, url_prefix='/api/job')


@job_bp.route('/create', methods=['POST'])
def create_job_description():
    """
    Create a new job description
    
    Expected JSON:
    {
        "recruiter_id": 1,
        "title": "Senior Python Developer",
        "company": "Tech Company",
        "description": "Job description text...",
        "required_skills": ["Python", "Django", "REST API"]
    }
    
    Returns:
        JSON with created job description
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recruiter_id', 'title', 'company', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Verify recruiter exists
        recruiter = Recruiter.query.get(data['recruiter_id'])
        if not recruiter:
            return jsonify({'error': 'Recruiter not found'}), 404
        
        # Extract skills from description if not provided
        skill_matcher = SkillMatcher()
        required_skills = data.get('required_skills', [])
        if not required_skills:
            # Try to extract skills from description
            required_skills = extract_skills_from_text(data['description'])
        
        extracted_data = {
            'required_skills': required_skills,
            'requirements': data.get('requirements'),
            'nice_to_have': data.get('nice_to_have')
        }
        
        # Create job description
        job_desc = DatabaseManager.create_job_description(
            recruiter_id=data['recruiter_id'],
            title=data['title'],
            company=data['company'],
            description=data['description'],
            extracted_data=extracted_data
        )
        
        return jsonify({
            'success': True,
            'message': 'Job description created successfully',
            'job_id': job_desc.id,
            'extracted_skills': required_skills
        }), 201
    
    except Exception as e:
        app_logger.error(f"Error creating job description: {str(e)}")
        return jsonify({'error': f'Error creating job description: {str(e)}'}), 500


@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job_description(job_id):
    """
    Get job description details
    
    Args:
        job_id: Job Description ID
    
    Returns:
        JSON with job details
    """
    try:
        job = JobDescription.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'description': job.description,
            'required_skills': job.required_skills,
            'requirements': job.requirements,
            'nice_to_have': job.nice_to_have,
            'is_processed': job.is_processed,
            'created_at': job.created_at.isoformat()
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving job description: {str(e)}")
        return jsonify({'error': f'Error retrieving job description: {str(e)}'}), 500


@job_bp.route('/', methods=['GET'])
def list_jobs():
    """
    List all job descriptions with pagination.

    Query parameters:
    - page: Page number (default 1)
    - per_page: Results per page (default 20)

    Returns:
        JSON with paginated jobs
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        pagination = JobDescription.query.order_by(
            JobDescription.created_at.desc()
        ).paginate(page=page, per_page=per_page)

        jobs = pagination.items

        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'jobs': [
                {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'created_at': job.created_at.isoformat(),
                    'candidate_count': len(job.rankings)
                }
                for job in jobs
            ]
        }), 200

    except Exception as e:
        app_logger.error(f"Error listing jobs: {str(e)}")
        return jsonify({'error': f'Error listing jobs: {str(e)}'}), 500


@job_bp.route('/recruiter/<int:recruiter_id>', methods=['GET'])
def get_recruiter_jobs(recruiter_id):
    """
    Get all jobs posted by a recruiter
    
    Args:
        recruiter_id: Recruiter ID
    
    Returns:
        JSON with list of jobs
    """
    try:
        recruiter = Recruiter.query.get(recruiter_id)
        if not recruiter:
            return jsonify({'error': 'Recruiter not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = JobDescription.query.filter_by(recruiter_id=recruiter_id).order_by(
            JobDescription.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        jobs = pagination.items
        
        return jsonify({
            'recruiter_id': recruiter_id,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'jobs': [
                {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'created_at': job.created_at.isoformat(),
                    'candidate_count': len(job.rankings)
                }
                for job in jobs
            ]
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving recruiter jobs: {str(e)}")
        return jsonify({'error': f'Error retrieving jobs: {str(e)}'}), 500


@job_bp.route('/<int:job_id>', methods=['PUT'])
def update_job_description(job_id):
    """
    Update a job description
    
    Args:
        job_id: Job Description ID
    
    Returns:
        JSON confirmation
    """
    try:
        job = JobDescription.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            job.title = data['title']
        if 'description' in data:
            job.description = data['description']
        if 'required_skills' in data:
            job.required_skills = data['required_skills']
        if 'requirements' in data:
            job.requirements = data['requirements']
        if 'nice_to_have' in data:
            job.nice_to_have = data['nice_to_have']
        
        db.session.commit()
        
        app_logger.info(f"Job description updated: {job_id}")
        
        return jsonify({
            'success': True,
            'message': 'Job description updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error updating job description: {str(e)}")
        return jsonify({'error': f'Error updating job description: {str(e)}'}), 500


@job_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job_description(job_id):
    """
    Delete a job description
    
    Args:
        job_id: Job Description ID
    
    Returns:
        JSON confirmation
    """
    try:
        job = JobDescription.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        db.session.delete(job)
        db.session.commit()
        
        app_logger.info(f"Job description deleted: {job_id}")
        
        return jsonify({
            'success': True,
            'message': 'Job description deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error deleting job description: {str(e)}")
        return jsonify({'error': f'Error deleting job description: {str(e)}'}), 500


@job_bp.route('/suitable', methods=['GET'])
def get_suitable_jobs():
    """
    Find suitable jobs for a candidate resume based on extracted skills.

    Query parameters:
    - candidate_id: Candidate ID (optional if resume_id is provided)
    - resume_id: Resume ID (preferred)
    - keyword: Optional keyword to narrow the job search

    Returns:
        JSON with ranked suitable jobs
    """
    try:
        candidate_id = request.args.get('candidate_id', type=int)
        resume_id = request.args.get('resume_id', type=int)
        keyword = request.args.get('keyword', '').strip().lower()

        resume = None

        if resume_id:
            resume = Resume.query.get(resume_id)
            if not resume:
                return jsonify({'error': 'Resume not found'}), 404
        elif candidate_id:
            candidate = Candidate.query.get(candidate_id)
            if not candidate:
                return jsonify({'error': 'Candidate not found'}), 404

            resume = Resume.query.filter_by(candidate_id=candidate_id).order_by(
                Resume.created_at.desc()
            ).first()
            if not resume:
                return jsonify({'error': 'No resumes found for this candidate'}), 404
        else:
            return jsonify({'error': 'resume_id or candidate_id is required'}), 400

        resume_skills = resume.skills or {}
        resume_skill_values = []
        if isinstance(resume_skills, dict):
            for skills in resume_skills.values():
                if isinstance(skills, list):
                    resume_skill_values.extend(skills)
        elif isinstance(resume_skills, list):
            resume_skill_values = resume_skills

        normalized_resume_skills = {skill.strip().lower() for skill in resume_skill_values if skill}
        skill_matcher = SkillMatcher()

        jobs = JobDescription.query.order_by(JobDescription.created_at.desc()).all()
        suitable_jobs = []

        for job in jobs:
            job_skills = job.required_skills or []
            if not job_skills:
                job_skills = skill_matcher.extract_skills_from_text(job.description, list(normalized_resume_skills))

            job_skill_values = [skill.strip() for skill in job_skills if skill]
            normalized_job_skills = [skill.lower() for skill in job_skill_values]

            if keyword:
                keyword_source = f"{job.title} {job.company} {job.description} {' '.join(job_skill_values)}".lower()
                if keyword not in keyword_source:
                    continue

            matched_skills = [skill for skill in job_skill_values if skill.lower() in normalized_resume_skills]
            missing_skills = [skill for skill in job_skill_values if skill.lower() not in normalized_resume_skills]

            if normalized_job_skills:
                match_score = (len(matched_skills) / len(normalized_job_skills)) * 100
            else:
                match_score = 0

            if matched_skills:
                recommendation = 'SUITABLE' if match_score >= 60 else 'POTENTIAL'
            else:
                recommendation = 'LOW_MATCH'

            suitable_jobs.append({
                'job_id': job.id,
                'title': job.title,
                'company': job.company,
                'description': job.description,
                'required_skills': job_skill_values,
                'match_score': round(match_score, 2),
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'recommendation': recommendation,
                'created_at': job.created_at.isoformat(),
            })

        suitable_jobs.sort(key=lambda item: item['match_score'], reverse=True)

        return jsonify({
            'success': True,
            'candidate_id': resume.candidate_id,
            'resume_id': resume.id,
            'resume_filename': resume.filename,
            'resume_skills': sorted(normalized_resume_skills),
            'total_jobs': len(suitable_jobs),
            'jobs': suitable_jobs,
        }), 200

    except Exception as e:
        app_logger.error(f"Error finding suitable jobs: {str(e)}")
        return jsonify({'error': f'Error finding suitable jobs: {str(e)}'}), 500


def extract_skills_from_text(text):
    """
    Extract skills from job description text
    
    Args:
        text: Job description text
    
    Returns:
        List of extracted skills
    """
    skills_list = []
    
    common_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue',
        'Django', 'Flask', 'Spring', 'Node.js', 'MySQL', 'MongoDB',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git',
        'REST API', 'GraphQL', 'SQL', 'NoSQL', 'CI/CD'
    ]
    
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            skills_list.append(skill)
    
    return list(set(skills_list))
