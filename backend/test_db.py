#!/usr/bin/env python
"""Test database connection"""

from app import app
from models.models import Candidate

print('Testing database connection...')

try:
    with app.app_context():
        result = Candidate.query.all()
        print(f'✓ Success! Found {len(result)} candidates')
except Exception as e:
    print(f'✗ Error: {str(e)}')
    import traceback
    traceback.print_exc()
