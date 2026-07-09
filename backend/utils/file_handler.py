"""
file_handler.py - File Upload and Processing Utilities
Handles file uploads, validation, and storage
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app
from utils.logger import app_logger


ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}


def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
    
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(file, max_size=None):
    """
    Validate uploaded file
    
    Args:
        file: Flask file object
        max_size: Maximum file size in bytes
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    if max_size is None:
        max_size = current_app.config.get('MAX_FILE_SIZE', 50000000)
    
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > max_size:
        return False, f"File size exceeds maximum allowed size: {max_size / 1024 / 1024:.1f} MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, "File is valid"


def save_uploaded_file(file, upload_folder=None):
    """
    Save uploaded file to disk
    
    Args:
        file: Flask file object
        upload_folder: Folder to save file to
    
    Returns:
        Tuple of (success, file_path_or_error_message)
    """
    try:
        # Validate file
        is_valid, message = validate_file(file)
        if not is_valid:
            return False, message
        
        # Get upload folder
        if upload_folder is None:
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
        
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file with secure filename
        filename = secure_filename(file.filename)
        timestamp = str(int(__import__('time').time()))
        filename = f"{timestamp}_{filename}"
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        app_logger.info(f"File saved successfully: {file_path}")
        return True, file_path
    
    except Exception as e:
        error_msg = f"Error saving file: {str(e)}"
        app_logger.error(error_msg)
        return False, error_msg


def get_file_extension(filename):
    """
    Get file extension
    
    Args:
        filename: Name of the file
    
    Returns:
        File extension
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ""


def delete_file(file_path):
    """
    Delete file from disk
    
    Args:
        file_path: Path to the file
    
    Returns:
        Boolean indicating success
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            app_logger.info(f"File deleted: {file_path}")
            return True
        else:
            app_logger.warning(f"File not found: {file_path}")
            return False
    except Exception as e:
        error_msg = f"Error deleting file: {str(e)}"
        app_logger.error(error_msg)
        return False
