"""
resume_routes.py - Resume Upload and Processing Routes
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
from models.models import db, Candidate, Resume
from modules.parser import ResumeParser
from utils.file_handler import save_uploaded_file
from utils.logger import app_logger
from utils.database import DatabaseManager
import os

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')


@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    Upload and process a resume file
    
    Expected form data:
    - file: Resume file (PDF/DOCX)
    - candidate_id: Optional candidate ID
    - full_name: Optional candidate full name
    - email: Optional candidate email
    
    Returns:
        JSON with upload and processing results
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Save file
        success, result = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
        if not success:
            return jsonify({'error': result}), 400
        
        file_path = result
        
        # Get or create candidate
        candidate_id = request.form.get('candidate_id')
        full_name = request.form.get('full_name', 'Unknown')
        email = request.form.get('email')
        
        if candidate_id:
            candidate = Candidate.query.get(candidate_id)
            if not candidate:
                return jsonify({'error': 'Candidate not found'}), 404
        else:
            candidate = DatabaseManager.create_candidate(
                full_name=full_name,
                email=email
            )
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_resume(file_path)
        
        # Extract file information
        file_type = file.filename.rsplit('.', 1)[1].lower()
        
        # Create resume record
        resume = DatabaseManager.create_resume(
            candidate_id=candidate.id,
            filename=file.filename,
            file_path=file_path,
            file_type=file_type,
            raw_text=parsed_data['raw_text'],
            parsed_data=parsed_data
        )
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and processed successfully',
            'candidate_id': candidate.id,
            'resume_id': resume.id,
            'parsed_data': {
                'skills': parsed_data.get('skills', {}),
                'experience': parsed_data.get('experience', {}),
                'education': parsed_data.get('education', []),
                'certifications': parsed_data.get('certifications', []),
                'contact_info': parsed_data.get('contact_info', {})
            }
        }), 201
    
    except Exception as e:
        app_logger.error(f"Error uploading resume: {str(e)}")
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500


@resume_bp.route('/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """
    Get resume details
    
    Args:
        resume_id: Resume ID
    
    Returns:
        JSON with resume details
    """
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify({
            'id': resume.id,
            'filename': resume.filename,
            'candidate_id': resume.candidate_id,
            'file_type': resume.file_type,
            'skills': resume.skills,
            'experience': resume.experience,
            'education': resume.education,
            'certifications': resume.certifications,
            'is_processed': resume.is_processed,
            'created_at': resume.created_at.isoformat()
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving resume: {str(e)}")
        return jsonify({'error': f'Error retrieving resume: {str(e)}'}), 500


@resume_bp.route('/<int:resume_id>/text', methods=['GET'])
def get_resume_text(resume_id):
    """
    Get raw text from resume
    
    Args:
        resume_id: Resume ID
    
    Returns:
        JSON with raw text
    """
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify({
            'resume_id': resume.id,
            'raw_text': resume.raw_text,
            'filename': resume.filename
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving resume text: {str(e)}")
        return jsonify({'error': f'Error retrieving resume text: {str(e)}'}), 500


@resume_bp.route('/candidate/<int:candidate_id>', methods=['GET'])
def get_candidate_resumes(candidate_id):
    """
    Get all resumes for a candidate
    
    Args:
        candidate_id: Candidate ID
    
    Returns:
        JSON with list of resumes
    """
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        resumes = candidate.resumes
        
        return jsonify({
            'candidate_id': candidate_id,
            'resumes': [
                {
                    'id': resume.id,
                    'filename': resume.filename,
                    'file_type': resume.file_type,
                    'created_at': resume.created_at.isoformat(),
                    'is_processed': resume.is_processed
                }
                for resume in resumes
            ]
        }), 200
    
    except Exception as e:
        app_logger.error(f"Error retrieving candidate resumes: {str(e)}")
        return jsonify({'error': f'Error retrieving resumes: {str(e)}'}), 500


@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """
    Delete a resume
    
    Args:
        resume_id: Resume ID
    
    Returns:
        JSON confirmation
    """
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Delete file
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        # Delete from database
        db.session.delete(resume)
        db.session.commit()
        
        app_logger.info(f"Resume deleted: {resume_id}")
        
        return jsonify({
            'success': True,
            'message': 'Resume deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"Error deleting resume: {str(e)}")
        return jsonify({'error': f'Error deleting resume: {str(e)}'}), 500
