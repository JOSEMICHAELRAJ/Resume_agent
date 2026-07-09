"""
candidate_routes.py - Candidate Management Routes
"""

from flask import Blueprint, request, jsonify
from models.models import db, Candidate, Resume
from utils.logger import app_logger
from utils.database import DatabaseManager

candidate_bp = Blueprint('candidate', __name__, url_prefix='/api/candidate')


@candidate_bp.route('/create', methods=['POST'])
def create_candidate():
    """
    Create a new candidate
    
    Expected JSON:
    {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "location": "New York"
    }
    
    Returns:
        JSON with created candidate
    """
    try:
        data = request.get_json()
        email = data.get('email')
        normalized_email = email.strip() if isinstance(email, str) else email
        if not normalized_email:
            normalized_email = None
        
        # Validate required fields
        if 'full_name' not in data:
            return jsonify({'error': 'full_name is required'}), 400
        
        # Check if candidate already exists
        if normalized_email:
            existing = Candidate.query.filter_by(email=normalized_email).first()
            if existing:
                return jsonify({'error': 'Candidate with this email already exists'}), 409
        
        # Create candidate
        candidate = DatabaseManager.create_candidate(
            full_name=data['full_name'],
            email=normalized_email,
            phone=data.get('phone'),
            location=data.get('location')
        )
        
        return jsonify({
            'success': True,
            'message': 'Candidate created successfully',
            'candidate_id': candidate.id,
            'candidate': {
                'id': candidate.id,
                'full_name': candidate.full_name,
                'email': candidate.email,
                'phone': candidate.phone,
                'location': candidate.location
            }
        }), 201
    
    except Exception as e:
        app_logger.error(f"Error creating candidate: {str(e)}")
        return jsonify({'error': f'Error creating candidate: {str(e)}'}), 500


@candidate_bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """
    Get candidate details
    
    Args:
        candidate_id: Candidate ID
    
    Returns:
        JSON with candidate details
    """
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        return jsonify({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'email': candidate.email,
            'phone': candidate.phone,
            'location': candidate.location,
            'summary': candidate.summary,
            'resumes_count': len(candidate.resumes),
            'created_at': candidate.created_at.isoformat()
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving candidate: {str(e)}")
        return jsonify({'error': f'Error retrieving candidate: {str(e)}'}), 500


@candidate_bp.route('/search', methods=['GET'])
def search_candidates():
    """
    Search for candidates
    
    Query parameters:
    - keyword: Search keyword (name or email)
    - limit: Maximum results (default 10)
    
    Returns:
        JSON with search results
    """
    try:
        keyword = request.args.get('keyword', '')
        limit = request.args.get('limit', 10, type=int)
        
        if not keyword:
            return jsonify({'error': 'keyword parameter is required'}), 400
        
        candidates = DatabaseManager.search_candidates(keyword, limit)
        
        return jsonify({
            'keyword': keyword,
            'total': len(candidates),
            'candidates': [
                {
                    'id': candidate.id,
                    'full_name': candidate.full_name,
                    'email': candidate.email,
                    'phone': candidate.phone,
                    'location': candidate.location
                }
                for candidate in candidates
            ]
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error searching candidates: {str(e)}")
        return jsonify({'error': f'Error searching candidates: {str(e)}'}), 500


@candidate_bp.route('/', methods=['GET'])
def list_candidates():
    """
    List all candidates with pagination
    
    Query parameters:
    - page: Page number (default 1)
    - per_page: Results per page (default 20)
    
    Returns:
        JSON with paginated candidates
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Candidate.query.order_by(
            Candidate.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        candidates = pagination.items
        
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'candidates': [
                {
                    'id': candidate.id,
                    'full_name': candidate.full_name,
                    'email': candidate.email,
                    'phone': candidate.phone,
                    'location': candidate.location,
                    'resumes_count': len(candidate.resumes)
                }
                for candidate in candidates
            ]
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error listing candidates: {str(e)}")
        return jsonify({'error': f'Error listing candidates: {str(e)}'}), 500


@candidate_bp.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """
    Update candidate information
    
    Expected JSON:
    {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "0987654321",
        "location": "Boston"
    }
    
    Args:
        candidate_id: Candidate ID
    
    Returns:
        JSON confirmation
    """
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            candidate.full_name = data['full_name']
        if 'email' in data:
            # Check if email is unique
            existing = Candidate.query.filter(
                (Candidate.email == data['email']) &
                (Candidate.id != candidate_id)
            ).first()
            if existing:
                return jsonify({'error': 'Email already in use'}), 409
            candidate.email = data['email']
        if 'phone' in data:
            candidate.phone = data['phone']
        if 'location' in data:
            candidate.location = data['location']
        if 'summary' in data:
            candidate.summary = data['summary']
        
        db.session.commit()
        app_logger.info(f"Candidate updated: {candidate_id}")
        
        return jsonify({
            'success': True,
            'message': 'Candidate updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error updating candidate: {str(e)}")
        return jsonify({'error': f'Error updating candidate: {str(e)}'}), 500


@candidate_bp.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """
    Delete a candidate
    
    Args:
        candidate_id: Candidate ID
    
    Returns:
        JSON confirmation
    """
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        db.session.delete(candidate)
        db.session.commit()
        
        app_logger.info(f"Candidate deleted: {candidate_id}")
        
        return jsonify({
            'success': True,
            'message': 'Candidate deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error deleting candidate: {str(e)}")
        return jsonify({'error': f'Error deleting candidate: {str(e)}'}), 500


@candidate_bp.route('/<int:candidate_id>/rankings/<int:job_id>', methods=['GET'])
def get_candidate_job_ranking(candidate_id, job_id):
    """
    Get candidate's ranking for a specific job
    
    Args:
        candidate_id: Candidate ID
        job_id: Job Description ID
    
    Returns:
        JSON with ranking details
    """
    try:
        from models.models import Ranking
        
        ranking = Ranking.query.filter_by(
            candidate_id=candidate_id,
            job_description_id=job_id
        ).first()
        
        if not ranking:
            return jsonify({'error': 'Ranking not found'}), 404
        
        return jsonify({
            'ranking_id': ranking.id,
            'candidate_id': candidate_id,
            'job_id': job_id,
            'overall_score': ranking.overall_score,
            'skill_match_score': ranking.skill_match_score,
            'experience_match_score': ranking.experience_match_score,
            'education_match_score': ranking.education_match_score,
            'semantic_similarity_score': ranking.semantic_similarity_score,
            'matched_skills': ranking.matched_skills,
            'missing_skills': ranking.missing_skills,
            'recommendation': ranking.recommendation
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving candidate ranking: {str(e)}")
        return jsonify({'error': f'Error retrieving ranking: {str(e)}'}), 500
