"""
app.py - Main Flask Application
Entry point for the Resume Screening System backend
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config.config import config
from models.models import db
from utils.logger import app_logger
from utils.database import DatabaseManager
from routes.resume_routes import resume_bp
from routes.job_routes import job_bp
from routes.matching_routes import matching_bp
from routes.candidate_routes import candidate_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config.get(env, config['default']))

# Initialize database
db.init_app(app)

# Initialize CORS
CORS(app, resources=app.config.get('CORS_RESOURCES', {}))

# Register blueprints (API routes)
app.register_blueprint(resume_bp)
app.register_blueprint(job_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(candidate_bp)


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request"""
    return jsonify({'error': 'Bad Request'}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    app_logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({'error': 'Internal Server Error'}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Try to connect to database
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        app_logger.error(f"Database health check failed: {str(e)}")
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'database': db_status,
        'version': '1.0.0'
    }), 200


# API info endpoint
@app.route('/api/info', methods=['GET'])
def info():
    """API information endpoint"""
    return jsonify({
        'name': 'Resume Screening AI Agent',
        'version': '1.0.0',
        'description': 'AI-powered resume screening and candidate ranking system',
        'endpoints': {
            'resume': '/api/resume/*',
            'job': '/api/job/*',
            'matching': '/api/matching/*',
            'candidate': '/api/candidate/*'
        }
    }), 200


# Before first request - Initialize database
@app.before_request
def create_tables():
    """Create database tables if they don't exist"""
    try:
        # This runs before the first request
        db.create_all()
    except Exception as e:
        app_logger.error(f"Error creating tables: {str(e)}")


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    app_logger.info(f"Starting Resume Screening API in {env} mode")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
