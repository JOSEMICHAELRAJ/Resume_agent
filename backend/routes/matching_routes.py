"""
matching_routes.py - Candidate Matching and Ranking Routes
"""

from flask import Blueprint, request, jsonify, current_app
from models.models import db, Resume, JobDescription, Ranking, Candidate
from modules.matcher import SemanticMatcher, SkillMatcher, ExperienceMatcher
from modules.ranking import CandidateRanker
from modules.ai_agent import ResumeAIAgent, FallbackAIAgent
from utils.logger import app_logger
from utils.database import DatabaseManager

matching_bp = Blueprint('matching', __name__, url_prefix='/api/matching')


@matching_bp.route('/match_candidates', methods=['POST'])
def match_candidates():
    """
    Match candidates against a job description
    
    Expected JSON:
    {
        "recruiter_id": 1,
        "job_id": 1,
        "resume_ids": [1, 2, 3]  # Optional, if not provided, match all candidates
    }
    
    Returns:
        JSON with matching results
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'recruiter_id' not in data or 'job_id' not in data:
            return jsonify({'error': 'Missing recruiter_id or job_id'}), 400
        
        recruiter_id = data['recruiter_id']
        job_id = data['job_id']
        resume_ids = data.get('resume_ids', [])
        
        # Get job description
        job = JobDescription.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        # Get resumes to match
        if resume_ids:
            resumes = Resume.query.filter(Resume.id.in_(resume_ids)).all()
        else:
            # Get all resumes
            resumes = Resume.query.all()
        
        if not resumes:
            return jsonify({'error': 'No resumes found to match'}), 404
        
        # Initialize matchers
        semantic_matcher = SemanticMatcher()
        skill_matcher = SkillMatcher()
        ranker = CandidateRanker()
        
        # Try to initialize AI agent, fallback if not available
        try:
            ai_agent = ResumeAIAgent()
            if not ai_agent.llm:
                ai_agent = FallbackAIAgent()
        except:
            ai_agent = FallbackAIAgent()
        
        job_text = job.description
        job_skills = job.required_skills or []
        
        results = []
        
        # Match each resume
        for resume in resumes:
            try:
                # Get candidate info
                candidate = resume.candidate
                
                # Calculate semantic similarity
                semantic_score = semantic_matcher.calculate_similarity(
                    job_text,
                    resume.raw_text or ""
                ) * 100  # Convert to 0-100 scale
                
                # Match skills
                skill_match_data = skill_matcher.match_skills(
                    resume.skills or {},
                    job_skills
                )
                skill_match_score = skill_match_data['match_percentage']
                
                # Match experience
                experience_data = ExperienceMatcher.match_experience(
                    resume.experience or {},
                    2  # Default 2 years requirement
                )
                experience_match_score = experience_data['match_score']
                
                # Calculate education match
                education_match_score = ranker.calculate_education_match(
                    resume.education or [],
                    job.requirements
                )
                
                # Calculate overall score
                scores = {
                    'skill_match_score': skill_match_score,
                    'experience_match_score': experience_match_score,
                    'education_match_score': education_match_score,
                    'semantic_similarity_score': semantic_score
                }
                
                overall_score = ranker.calculate_overall_score(scores)
                
                # Get recommendation
                recommendation = ranker.get_recommendation(
                    overall_score,
                    skill_match_score
                )
                
                # Generate AI insights
                summary = ai_agent.generate_candidate_summary(
                    resume.raw_text or "",
                    job_text
                )
                
                interview_questions = ai_agent.generate_interview_questions(
                    resume.raw_text or "",
                    skill_match_data.get('missing_skills', []),
                    job.title
                )
                
                # Prepare result
                result = {
                    'candidate_id': candidate.id,
                    'candidate_name': candidate.full_name,
                    'resume_id': resume.id,
                    'overall_score': overall_score,
                    'skill_match_score': skill_match_score,
                    'experience_match_score': experience_match_score,
                    'education_match_score': education_match_score,
                    'semantic_similarity_score': semantic_score,
                    'matched_skills': skill_match_data['matched_skills'],
                    'missing_skills': skill_match_data['missing_skills'],
                    'experience_years': experience_data['resume_years'],
                    'summary': summary,
                    'interview_questions': interview_questions,
                    'recommendation': recommendation
                }
                
                # Store in database
                ranking = DatabaseManager.create_ranking(
                    recruiter_id=recruiter_id,
                    candidate_id=candidate.id,
                    job_description_id=job_id,
                    resume_id=resume.id,
                    scores={**result}
                )
                
                result['ranking_id'] = ranking.id
                results.append(result)
            
            except Exception as e:
                app_logger.error(f"Error matching resume {resume.id}: {str(e)}")
                continue
        
        # Sort by score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Assign ranks
        for i, result in enumerate(results, 1):
            result['rank'] = i
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'total_matches': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error in candidate matching: {str(e)}")
        return jsonify({'error': f'Error matching candidates: {str(e)}'}), 500


@matching_bp.route('/ranking/<int:job_id>', methods=['GET'])
def get_job_rankings(job_id):
    """
    Get all rankings for a job
    
    Args:
        job_id: Job Description ID
    
    Returns:
        JSON with rankings
    """
    try:
        job = JobDescription.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get rankings
        pagination = Ranking.query.filter_by(
            job_description_id=job_id
        ).order_by(Ranking.overall_score.desc()).paginate(
            page=page, per_page=per_page
        )
        
        rankings = pagination.items
        
        result_data = []
        for ranking in rankings:
            candidate = ranking.candidate
            result_data.append({
                'ranking_id': ranking.id,
                'candidate_id': candidate.id,
                'candidate_name': candidate.full_name,
                'candidate_email': candidate.email,
                'overall_score': ranking.overall_score,
                'skill_match_score': ranking.skill_match_score,
                'experience_match_score': ranking.experience_match_score,
                'education_match_score': ranking.education_match_score,
                'semantic_similarity_score': ranking.semantic_similarity_score,
                'matched_skills': ranking.matched_skills,
                'missing_skills': ranking.missing_skills,
                'recommendation': ranking.recommendation,
                'created_at': ranking.created_at.isoformat()
            })
        
        return jsonify({
            'job_id': job_id,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'rankings': result_data
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving rankings: {str(e)}")
        return jsonify({'error': f'Error retrieving rankings: {str(e)}'}), 500


@matching_bp.route('/ranking/<int:ranking_id>', methods=['GET'])
def get_ranking_details(ranking_id):
    """
    Get detailed ranking information
    
    Args:
        ranking_id: Ranking ID
    
    Returns:
        JSON with ranking details
    """
    try:
        ranking = Ranking.query.get(ranking_id)
        if not ranking:
            return jsonify({'error': 'Ranking not found'}), 404
        
        candidate = ranking.candidate
        job = ranking.job_description
        
        return jsonify({
            'ranking_id': ranking.id,
            'candidate': {
                'id': candidate.id,
                'name': candidate.full_name,
                'email': candidate.email,
                'phone': candidate.phone,
                'location': candidate.location
            },
            'job': {
                'id': job.id,
                'title': job.title,
                'company': job.company
            },
            'scores': {
                'overall_score': ranking.overall_score,
                'skill_match_score': ranking.skill_match_score,
                'experience_match_score': ranking.experience_match_score,
                'education_match_score': ranking.education_match_score,
                'semantic_similarity_score': ranking.semantic_similarity_score
            },
            'matched_skills': ranking.matched_skills,
            'missing_skills': ranking.missing_skills,
            'experience_years': ranking.experience_years,
            'summary': ranking.summary,
            'interview_questions': ranking.interview_questions,
            'recommendation': ranking.recommendation,
            'created_at': ranking.created_at.isoformat()
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving ranking details: {str(e)}")
        return jsonify({'error': f'Error retrieving ranking details: {str(e)}'}), 500


@matching_bp.route('/ranking/<int:ranking_id>', methods=['PUT'])
def update_ranking_recommendation(ranking_id):
    """
    Update ranking recommendation
    
    Expected JSON:
    {
        "recommendation": "SHORTLIST" or "REJECT"
    }
    
    Args:
        ranking_id: Ranking ID
    
    Returns:
        JSON confirmation
    """
    try:
        ranking = Ranking.query.get(ranking_id)
        if not ranking:
            return jsonify({'error': 'Ranking not found'}), 404
        
        data = request.get_json()
        if 'recommendation' in data:
            ranking.recommendation = data['recommendation']
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation updated successfully',
            'ranking_id': ranking.id,
            'recommendation': ranking.recommendation
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error updating recommendation: {str(e)}")
        return jsonify({'error': f'Error updating recommendation: {str(e)}'}), 500
