# Quick Start Guide

Get the Resume Screening AI System running in minutes.

## 30-Minute Quick Start

### Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] MySQL 5.7+ running
- [ ] OpenAI API key available
- [ ] Git installed

### Step 1: Setup Database (2 minutes)

```bash
mysql -u root -p
```

Paste into MySQL console:
```sql
CREATE DATABASE resume_screening_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 2: Backend Setup (8 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `backend/.env`:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=resume_screening_db
OPENAI_API_KEY=sk-your-openai-key
```

**Start backend:**
```bash
python app.py
```

✅ Backend running at http://localhost:5000

### Step 3: Frontend Setup (8 minutes)

**Open new terminal:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

✅ Frontend will open at http://localhost:3000

### Step 4: Verify Installation (5 minutes)

**In browser:**
1. Go to http://localhost:3000
2. You should see the Dashboard
3. Navigate to each page
4. Check backend connection status (top right)

## Quick Test Workflow

### 1. Upload a Resume (1 min)
- Go to "Upload Resumes"
- Drag and drop a PDF or DOCX file
- Fill in candidate info
- Click "Upload"

### 2. Create a Job (1 min)
- Go to "Create Job"
- Fill in:
  - Job Title: "Senior Developer"
  - Company: "Tech Corp"
  - Description: "Looking for experienced developer..."
  - Skills: "Python, JavaScript, React, SQL"
- Click "Create Job"

### 3. Match Candidates (1 min)
- Go to "Jobs"
- Click on the job you just created
- System automatically matches candidates
- Review the ranked list

### 4. Review Details (1 min)
- Click on a candidate ranking
- View scores and skills analysis
- Read AI-generated summary
- Click "Shortlist" or "Reject"

## Common Commands

### Backend
```bash
# Activate environment (if not already)
cd backend
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Start server
python app.py

# See logs
tail -f logs/app.log

# Stop server
CTRL+C
```

### Frontend
```bash
cd frontend

# Start development
npm start

# Build production version
npm run build

# Stop server
CTRL+C
```

## Stopping & Restarting

### Stop All Services
```bash
# Terminal 1 (Backend): CTRL+C
# Terminal 2 (Frontend): CTRL+C
# MySQL: Usually keeps running
```

### Restart Everything
```bash
# Terminal 1
cd backend
source venv/bin/activate
python app.py

# Terminal 2 (New window)
cd frontend
npm start
```

## Useful Links

- **Backend API**: http://localhost:5000/api
- **Frontend**: http://localhost:3000
- **API Info**: http://localhost:5000/api/info
- **Health Check**: http://localhost:5000/api/health

## Testing API with cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Get API info
curl http://localhost:5000/api/info

# List candidates
curl http://localhost:5000/api/candidates/

# List jobs
curl http://localhost:5000/api/jobs/
```

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Port 5000 in use | `lsof -ti:5000 \| xargs kill -9` (Mac/Linux) or use netstat on Windows |
| Port 3000 in use | `lsof -ti:3000 \| xargs kill -9` (Mac/Linux) or use netstat on Windows |
| Database not found | Run: `CREATE DATABASE resume_screening_db;` |
| Module not found | Run: `pip install -r requirements.txt` or `npm install` |
| API not responding | Verify backend is running: `curl http://localhost:5000/api/health` |
| Frontend can't connect to API | Check `REACT_APP_API_URL` in `frontend/.env` |

## Full Documentation

For detailed documentation, see:
- [Installation Guide](./INSTALLATION.md) - Comprehensive setup instructions
- [Backend README](./backend/README.md) - Backend architecture and API docs
- [Frontend README](./frontend/README.md) - Frontend components and guides
- [Main README](./README.md) - Complete system overview

## Next Steps

1. ✅ Run the system locally
2. 📝 Upload sample resumes
3. 💼 Create test job descriptions
4. 🤖 Test the matching algorithm
5. 🔧 Customize scoring weights
6. 🚀 Deploy to production

---

**Stuck?** Check the [Installation Guide](./INSTALLATION.md) for detailed troubleshooting.

Happy screening! 🚀
