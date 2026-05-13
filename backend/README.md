# Resume Screening AI Agent - Backend

Backend server for the Resume Screening and Candidate Recommendation System built with Flask, AI/ML, and MySQL.

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config/
│   ├── config.py         # Configuration settings
│   └── __init__.py
├── models/
│   ├── models.py         # SQLAlchemy database models
│   └── __init__.py
├── modules/
│   ├── parser.py         # Resume parser (PDF/DOCX)
│   ├── matcher.py        # Semantic matching engine
│   ├── ranking.py        # Candidate ranking logic
│   ├── ai_agent.py       # AI agent (LangChain + OpenAI)
│   └── __init__.py
├── routes/
│   ├── resume_routes.py      # Resume API endpoints
│   ├── job_routes.py         # Job description endpoints
│   ├── matching_routes.py    # Matching and ranking endpoints
│   ├── candidate_routes.py   # Candidate management endpoints
│   └── __init__.py
├── utils/
│   ├── logger.py           # Logging configuration
│   ├── file_handler.py     # File upload utilities
│   ├── database.py         # Database utilities
│   └── __init__.py
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## Installation

### 1. Clone the repository
```bash
cd backend
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
# Copy .env file and update values
cp .env.example .env
```

Edit `.env` with your configuration:
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` - MySQL credentials
- `OPENAI_API_KEY` - OpenAI API key
- `SECRET_KEY` - Flask secret key
- `FRONTEND_URL` - Frontend URL for CORS

### 5. Create MySQL database
```sql
CREATE DATABASE resume_screening_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run the application
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Resume Endpoints
- `POST /api/resume/upload` - Upload and process resume
- `GET /api/resume/<resume_id>` - Get resume details
- `GET /api/resume/<resume_id>/text` - Get raw resume text
- `GET /api/resume/candidate/<candidate_id>` - Get all resumes for candidate
- `DELETE /api/resume/<resume_id>` - Delete resume

### Job Description Endpoints
- `POST /api/job/create` - Create new job description
- `GET /api/job/<job_id>` - Get job details
- `GET /api/job/recruiter/<recruiter_id>` - Get recruiter's jobs
- `PUT /api/job/<job_id>` - Update job description
- `DELETE /api/job/<job_id>` - Delete job description

### Candidate Endpoints
- `POST /api/candidate/create` - Create new candidate
- `GET /api/candidate/<candidate_id>` - Get candidate details
- `GET /api/candidate/search` - Search candidates
- `GET /api/candidate` - List all candidates
- `PUT /api/candidate/<candidate_id>` - Update candidate
- `DELETE /api/candidate/<candidate_id>` - Delete candidate
- `GET /api/candidate/<candidate_id>/rankings/<job_id>` - Get candidate's ranking for job

### Matching & Ranking Endpoints
- `POST /api/matching/match_candidates` - Match candidates to job
- `GET /api/matching/ranking/<job_id>` - Get all rankings for job
- `GET /api/matching/ranking/<ranking_id>` - Get ranking details
- `PUT /api/matching/ranking/<ranking_id>` - Update ranking recommendation

### System Endpoints
- `GET /api/health` - Health check
- `GET /api/info` - API information

## Features

### Resume Processing
- **PDF/DOCX Support** - Automatically extract text from PDF and DOCX files
- **Information Extraction** - Extract skills, experience, education, certifications
- **Contact Information** - Extract email, phone, LinkedIn profile

### Semantic Matching
- **Embedding-based Matching** - Uses Sentence Transformers for semantic similarity
- **Skill Matching** - Matches required skills vs. candidate skills
- **Experience Matching** - Compares years of experience
- **Education Matching** - Validates education requirements

### Candidate Ranking
- **Multi-factor Scoring** - Combines multiple scoring metrics
  - Skill Match (40%)
  - Experience Match (25%)
  - Education Match (15%)
  - Semantic Similarity (20%)
- **Recommendations** - SHORTLIST, PENDING, or REJECT

### AI-Powered Insights
- **Candidate Summaries** - AI-generated candidate fit assessment
- **Interview Questions** - Generated based on missing skills
- **Improvement Suggestions** - Recommendations for candidates

## Configuration

### Environment Variables

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=resume_screening_db
DB_PORT=3306

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# File Upload
MAX_FILE_SIZE=50000000
UPLOAD_FOLDER=../resumes
ALLOWED_EXTENSIONS=pdf,docx

# AI/ML
EMBEDDING_MODEL=all-MiniLM-L6-v2

# CORS
FRONTEND_URL=http://localhost:3000
```

## Database Schema

### Tables
- **recruiters** - User accounts
- **candidates** - Candidate profiles
- **resumes** - Uploaded resume documents
- **job_descriptions** - Job postings
- **rankings** - Candidate-job matches with scores

## Modules

### parser.py
Extracts information from resume files:
- Text extraction from PDF/DOCX
- Skill identification
- Experience calculation
- Education extraction
- Certification detection

### matcher.py
Semantic matching between resumes and jobs:
- Sentence Transformer embeddings
- Cosine similarity scoring
- Skill matching with semantic similarity
- Experience comparison

### ranking.py
Ranks candidates based on multiple factors:
- Weighted scoring system
- Overall score calculation
- Recommendation generation
- Ranking summary statistics

### ai_agent.py
AI-powered insights using LangChain and OpenAI:
- Candidate summary generation
- Interview question generation
- Improvement suggestions
- Fallback responses when OpenAI unavailable

## Development

### Run tests (when added)
```bash
pytest tests/
```

### Format code
```bash
black .
flake8 .
```

### Generate requirements
```bash
pip freeze > requirements.txt
```

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check DB credentials in `.env`
- Ensure database exists

### OpenAI API Error
- Verify API key is valid
- Check OpenAI account has credits
- System will fallback to template responses

### File Upload Error
- Check `UPLOAD_FOLDER` permissions
- Verify file is PDF or DOCX
- Check file size limit

### Model Loading Error
- Sentence Transformers will download model on first run
- Requires internet connection
- Ensure sufficient disk space

## Performance Optimization

- Database connection pooling enabled
- SQLAlchemy query optimization
- Lazy loading for relationships
- File size validation
- Batch processing support

## Security

- Environment variables for sensitive data
- File type validation
- SQL injection prevention (SQLAlchemy)
- CORS enabled for frontend
- Password hashing (to be implemented)
- Input validation on all endpoints

## Future Enhancements

- User authentication and JWT tokens
- Advanced NLP processing
- Custom skill taxonomy
- Bulk candidate import
- Report generation
- Email notifications
- Interview scheduling
- Candidate portal

## License

MIT License

## Support

For issues or questions, please contact the development team.
