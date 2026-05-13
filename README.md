# AI-Powered Resume Screening and Candidate Ranking System

A complete web application that automatically screens resumes, compares them with job descriptions, ranks candidates, and provides recruiter-friendly insights using AI and machine learning.

## 🎯 Overview

This system leverages advanced NLP, semantic similarity matching, and AI-powered insights to:
- **Automatically extract** information from resumes (skills, experience, education)
- **Intelligently match** candidates against job requirements
- **Rank candidates** using multi-factor scoring
- **Generate insights** including interview questions and improvement suggestions
- **Streamline recruitment** with a modern, intuitive dashboard

## 🏗️ Project Architecture

```
resume-agent/
├── backend/                 # Flask REST API
│   ├── app.py              # Main application
│   ├── config/             # Configuration
│   ├── models/             # Database models
│   ├── modules/            # Core modules
│   │   ├── parser.py       # Resume parser
│   │   ├── matcher.py      # Semantic matching
│   │   ├── ranking.py      # Ranking algorithm
│   │   └── ai_agent.py     # AI insights
│   ├── routes/             # API endpoints
│   ├── utils/              # Utilities
│   └── requirements.txt    # Dependencies
├── frontend/               # React Dashboard
│   ├── public/             # Static files
│   ├── src/                # React components
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Utilities
│   └── package.json        # Dependencies
├── resumes/                # Uploaded resume storage
└── README.md              # This file
```

## ✨ Key Features

### 1. Resume Processing
- 📄 **PDF & DOCX Support** - Parse both document formats
- 🔍 **Information Extraction** - Skills, experience, education, certifications
- 📍 **Contact Info** - Email, phone, LinkedIn profiles
- 🏗️ **Structured Data** - Organized extracted information

### 2. Semantic Matching
- 🤖 **AI-Powered Matching** - Uses Sentence Transformers for embeddings
- 🎯 **Skill Matching** - Matches required vs candidate skills
- 📊 **Experience Comparison** - Years of experience analysis
- 🎓 **Education Validation** - Educational requirement checks
- 📈 **Cosine Similarity** - Advanced similarity scoring

### 3. Intelligent Ranking
- ⭐ **Multi-Factor Scoring**
  - Skill Match: 40%
  - Experience Match: 25%
  - Education Match: 15%
  - Semantic Similarity: 20%
- 🏆 **Automated Recommendations** - SHORTLIST, PENDING, REJECT
- 📋 **Detailed Rankings** - Sortable, filterable results

### 4. AI-Powered Insights
- 💭 **Candidate Summaries** - AI-generated fit assessments
- ❓ **Interview Questions** - Auto-generated based on role
- 💡 **Improvement Suggestions** - Recommendations for candidates
- 🔗 **LangChain Integration** - Advanced NLP capabilities

### 5. Modern Dashboard
- 📊 **Interactive Charts** - Candidate rankings visualization
- 🔍 **Search & Filter** - Find candidates quickly
- 📱 **Responsive Design** - Mobile-friendly interface
- 🎨 **Professional UI** - Tailwind CSS + DaisyUI
- ⚡ **Real-time Updates** - Live data synchronization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env .env.local
# Edit .env.local with your credentials

# Create database
mysql -u root -p
CREATE DATABASE resume_screening_db CHARACTER SET utf8mb4;

# Run the server
python app.py
```

Backend will be available at: `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env .env.local
# Edit .env.local if needed

# Start development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## 📝 API Documentation

### Authentication (To Be Implemented)
```
Bearer Token in Authorization header
```

### Resume Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/upload` | Upload and process resume |
| GET | `/api/resume/<id>` | Get resume details |
| GET | `/api/resume/<id>/text` | Get raw resume text |
| DELETE | `/api/resume/<id>` | Delete resume |

### Job Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/job/create` | Create job description |
| GET | `/api/job/<id>` | Get job details |
| GET | `/api/job/recruiter/<id>` | List recruiter's jobs |
| PUT | `/api/job/<id>` | Update job |
| DELETE | `/api/job/<id>` | Delete job |

### Candidate Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/candidate/create` | Create candidate |
| GET | `/api/candidate/<id>` | Get candidate details |
| GET | `/api/candidate/search` | Search candidates |
| PUT | `/api/candidate/<id>` | Update candidate |
| DELETE | `/api/candidate/<id>` | Delete candidate |

### Matching Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/matching/match_candidates` | Match candidates to job |
| GET | `/api/matching/ranking/<jobId>` | Get job rankings |
| GET | `/api/matching/ranking/<rankingId>` | Get ranking details |
| PUT | `/api/matching/ranking/<rankingId>` | Update recommendation |

### System Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/info` | API information |

## 🔧 Configuration

### Backend (.env)
```env
FLASK_ENV=development
OPENAI_API_KEY=sk-...
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=resume_screening_db
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

## 🗄️ Database Schema

### Tables
- **recruiters** - User accounts for recruiters
- **candidates** - Candidate profiles
- **resumes** - Uploaded resume documents
- **job_descriptions** - Job postings
- **rankings** - Candidate-job matches with scores

[See detailed schema in backend README](./backend/README.md)

## 💻 Technology Stack

### Backend
- **Framework**: Flask 2.3.0
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **NLP**: LangChain, OpenAI API
- **Embeddings**: Sentence Transformers
- **PDF Processing**: PyPDF2, pdfplumber
- **Document Processing**: python-docx

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **Styling**: Tailwind CSS, DaisyUI
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast

## 📊 Database Models

### Recruiter
```python
- id (PK)
- username, email, password_hash
- full_name, company, department
- is_active, created_at, updated_at
```

### Candidate
```python
- id (PK)
- full_name, email, phone, location
- summary, created_at, updated_at
```

### Resume
```python
- id (PK)
- candidate_id (FK), filename, file_path
- skills, experience, education, certifications
- is_processed, created_at, updated_at
```

### JobDescription
```python
- id (PK)
- recruiter_id (FK), title, company
- description, required_skills
- is_processed, created_at, updated_at
```

### Ranking
```python
- id (PK)
- candidate_id, job_description_id (FKs)
- overall_score, skill_match_score, etc.
- matched_skills, missing_skills
- summary, interview_questions
- recommendation (SHORTLIST/PENDING/REJECT)
```

## 🔄 Workflow

```
1. Recruiter Creates Account
        ↓
2. Recruiter Uploads Job Description
        ↓
3. System Extracts Job Requirements
        ↓
4. Candidates Upload Resumes (PDF/DOCX)
        ↓
5. System Extracts Resume Information
        ↓
6. AI Matches Candidates to Job
        ├─ Skill Matching (Semantic + Keyword)
        ├─ Experience Comparison
        ├─ Education Validation
        └─ Semantic Similarity
        ↓
7. System Ranks Candidates (Multi-factor scoring)
        ↓
8. AI Generates Insights
        ├─ Candidate Summaries
        ├─ Interview Questions
        └─ Improvement Suggestions
        ↓
9. Recruiter Reviews & Makes Recommendations
        ├─ SHORTLIST
        ├─ PENDING
        └─ REJECT
        ↓
10. Export & Take Action
```

## 📈 Scoring Algorithm

### Overall Score Calculation
```
Overall Score = (
    Skill Match Score × 0.40 +
    Experience Match Score × 0.25 +
    Education Match Score × 0.15 +
    Semantic Similarity Score × 0.20
)
```

### Score Ranges
- **75-100**: SHORTLIST - Highly qualified candidates
- **50-74**: PENDING - Review candidates
- **0-49**: REJECT - Not a good fit

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Docker Setup
```bash
# Build backend image
docker build -t resume-api ./backend

# Build frontend image
docker build -t resume-ui ./frontend

# Run with docker-compose
docker-compose up
```

### Production Deployment

**Backend (Heroku)**
```bash
git push heroku main
```

**Frontend (Vercel)**
```bash
vercel --prod
```

**Full Stack (AWS)**
- Backend on EC2 with Nginx reverse proxy
- Frontend on CloudFront + S3
- RDS for MySQL database

See [Deployment Guide](./docs/DEPLOYMENT.md) for detailed steps.

## 🔒 Security

- ✅ Environment variables for sensitive data
- ✅ HTTPS/TLS encryption
- ✅ CORS enabled for frontend domain
- ✅ SQL injection protection (SQLAlchemy)
- ✅ XSS protection (React escaping)
- ✅ File type validation
- ✅ Rate limiting ready
- ✅ Input validation on client and server

Protected endpoints require authentication (to be implemented):
- JWT tokens
- Refresh token rotation
- Secure cookie handling

## 📚 Documentation

- [Backend README](./backend/README.md) - Backend setup and API docs
- [Frontend README](./frontend/README.md) - Frontend setup and components
- [Deployment Guide](./docs/DEPLOYMENT.md) - Production deployment
- [API Documentation](./docs/API.md) - Complete API reference

## 🐛 Troubleshooting

### Backend Issues
See [Backend Troubleshooting](./backend/README.md#troubleshooting)

### Frontend Issues
See [Frontend Troubleshooting](./frontend/README.md#troubleshooting)

### Database Issues
- Verify MySQL is running
- Check credentials in .env
- Ensure database exists
- Check network connectivity

## 🤝 Contributing

1. Clone the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📊 Performance Metrics

Target metrics:
- Backend API response time: < 500ms
- Frontend load time: < 3s
- Lighthouse score: > 85
- Database query time: < 100ms

## 🔮 Future Roadmap

- [ ] User authentication and authorization
- [ ] Advanced NLP models
- [ ] Bulk resume import
- [ ] Email notifications
- [ ] Interview scheduling
- [ ] Video interview integration
- [ ] Anonymous scoring
- [ ] Team collaboration
- [ ] Custom scoring rules
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Webhook integrations

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 👥 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Review documentation
3. Create a new issue with detailed description
4. Contact the development team

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo API
- Sentence Transformers for embeddings
- Flask and React communities
- Contributors and testers

---

**Happy Recruiting! 🎯**

Built with ❤️ by the ResumeAI Team
