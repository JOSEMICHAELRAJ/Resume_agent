<<<<<<< HEAD
# Installation & Setup Guide

Complete step-by-step guide to install and run the Resume Screening AI System.

## Prerequisites

Before starting, ensure you have installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **MySQL 5.7+** - [Download](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download](https://git-scm.com/)

### Verify Installations

```bash
python --version
node --version
npm --version
mysql --version
git --version
```

## Step 1: Setup Database

### Create MySQL Database

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE resume_screening_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

## Step 2: Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - DB credentials
# - OpenAI API key
# - Secret key
```

**Important Environment Variables:**
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=resume_screening_db
DB_PORT=3306

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Frontend
FRONTEND_URL=http://localhost:3000
```

### 5. Create Logs Directory

```bash
mkdir logs
```

### 6. Run Backend Server

```bash
python app.py
```

The backend will start at: **http://localhost:5000**

### Verify Backend

Open in browser or terminal:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "version": "1.0.0"
}
```

## Step 3: Frontend Setup

### 1. Open New Terminal and Navigate to Frontend

```bash
cd frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This will install all required packages including:
- React
- React Router
- Tailwind CSS
- Axios
- Recharts
- And other dependencies

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env (usually no changes needed for local development)
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### 4. Start Frontend Development Server

```bash
npm start
```

The frontend will open automatically at: **http://localhost:3000**

> If it doesn't open automatically, navigate to `http://localhost:3000` in your browser.

## Step 4: Verify Installation

### Checklist

- [ ] Backend running at `http://localhost:5000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] Database connected successfully
- [ ] No error messages in console
- [ ] Can access dashboard

### Test API Connection

```bash
# Terminal 1: Backend is running
# Terminal 2: Frontend is running
# Terminal 3: Test API

curl http://localhost:5000/api/info
```

Expected response:
```json
{
  "name": "Resume Screening AI Agent",
  "version": "1.0.0",
  "description": "AI-powered resume screening and candidate ranking system",
  "endpoints": {...}
}
```

## Step 5: First Usage

### Create Initial Data

1. **Upload Resumes**
   - Go to "Upload Resumes" tab
   - Drag and drop PDF/DOCX files
   - Add candidate information
   - Click "Upload"

2. **Create Job Description**
   - Go to "Create Job" tab
   - Fill in job details
   - Add required skills
   - Click "Create Job"

3. **Match Candidates**
   - Go to "Jobs" tab
   - Select a job
   - System will match candidates
   - Review results

4. **Review Rankings**
   - View candidate rankings
   - Check scores and skills
   - Read AI-generated summaries
   - Make recommendations

## Troubleshooting

### Backend Issues

**Port 5000 Already in Use**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Database Connection Error**
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1"

# Verify credentials in .env
# Check database exists
mysql -u root -p -e "SHOW DATABASES;"
```

**Module Not Found**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**API Returns 500 Error**
- Check backend console for error messages
- Verify database connection
- Check environment variables
- Review `logs/app.log` file

### Frontend Issues

**Port 3000 Already in Use**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

**Module Not Found**
```bash
rm -rf node_modules package-lock.json
npm install
```

**API Not Connecting**
- Verify backend is running
- Check `REACT_APP_API_URL` in .env
- Check browser console for errors (F12)
- Verify CORS is enabled in backend

**Styles Not Loading**
```bash
npm run build
npm start
```

### Common Issues

**"Cannot connect to database"**
1. Verify MySQL service is running
2. Check credentials in .env
3. Create database: `CREATE DATABASE resume_screening_db;`
4. Restart backend server

**"ImportError: No module named..."**
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt`
3. Check Python version (3.8+)

**"Module '@module' not found" (Frontend)**
1. Delete `node_modules` folder
2. Delete `package-lock.json`
3. Run `npm install`

## Development Commands

### Backend

```bash
# Start development server
python app.py

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

### Frontend

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Production Deployment

See [Production Deployment Guide](./DEPLOYMENT.md) for:
- Docker containerization
- Cloud deployment (AWS, Heroku, Vercel)
- Performance optimization
- Security hardening

## Need Help?

1. Check [Backend README](./backend/README.md)
2. Check [Frontend README](./frontend/README.md)
3. Review [Main README](./README.md)
4. Check logs in `backend/logs/`
5. Review error messages in browser console (F12)

## Next Steps

After successful installation:

1. **Read Documentation**
   - Backend API docs
   - Frontend components guide
   - Database schema

2. **Explore Features**
   - Upload sample resumes
   - Create job descriptions
   - Test matching algorithm

3. **Customize**
   - Modify scoring weights in `ranking.py`
   - Adjust AI prompts in `ai_agent.py`
   - Customize UI in React components

4. **Deploy**
   - Set up production environment
   - Configure SSL/TLS
   - Set up CI/CD pipeline

---

Happy building! 🚀
=======
# Installation & Setup Guide

Complete step-by-step guide to install and run the Resume Screening AI System.

## Prerequisites

Before starting, ensure you have installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **MySQL 5.7+** - [Download](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download](https://git-scm.com/)

### Verify Installations

```bash
python --version
node --version
npm --version
mysql --version
git --version
```

## Step 1: Setup Database

### Create MySQL Database

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE resume_screening_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

## Step 2: Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - DB credentials
# - OpenAI API key
# - Secret key
```

**Important Environment Variables:**
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=resume_screening_db
DB_PORT=3306

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Frontend
FRONTEND_URL=http://localhost:3000
```

### 5. Create Logs Directory

```bash
mkdir logs
```

### 6. Run Backend Server

```bash
python app.py
```

The backend will start at: **http://localhost:5000**

### Verify Backend

Open in browser or terminal:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "version": "1.0.0"
}
```

## Step 3: Frontend Setup

### 1. Open New Terminal and Navigate to Frontend

```bash
cd frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This will install all required packages including:
- React
- React Router
- Tailwind CSS
- Axios
- Recharts
- And other dependencies

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env (usually no changes needed for local development)
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### 4. Start Frontend Development Server

```bash
npm start
```

The frontend will open automatically at: **http://localhost:3000**

> If it doesn't open automatically, navigate to `http://localhost:3000` in your browser.

## Step 4: Verify Installation

### Checklist

- [ ] Backend running at `http://localhost:5000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] Database connected successfully
- [ ] No error messages in console
- [ ] Can access dashboard

### Test API Connection

```bash
# Terminal 1: Backend is running
# Terminal 2: Frontend is running
# Terminal 3: Test API

curl http://localhost:5000/api/info
```

Expected response:
```json
{
  "name": "Resume Screening AI Agent",
  "version": "1.0.0",
  "description": "AI-powered resume screening and candidate ranking system",
  "endpoints": {...}
}
```

## Step 5: First Usage

### Create Initial Data

1. **Upload Resumes**
   - Go to "Upload Resumes" tab
   - Drag and drop PDF/DOCX files
   - Add candidate information
   - Click "Upload"

2. **Create Job Description**
   - Go to "Create Job" tab
   - Fill in job details
   - Add required skills
   - Click "Create Job"

3. **Match Candidates**
   - Go to "Jobs" tab
   - Select a job
   - System will match candidates
   - Review results

4. **Review Rankings**
   - View candidate rankings
   - Check scores and skills
   - Read AI-generated summaries
   - Make recommendations

## Troubleshooting

### Backend Issues

**Port 5000 Already in Use**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Database Connection Error**
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1"

# Verify credentials in .env
# Check database exists
mysql -u root -p -e "SHOW DATABASES;"
```

**Module Not Found**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**API Returns 500 Error**
- Check backend console for error messages
- Verify database connection
- Check environment variables
- Review `logs/app.log` file

### Frontend Issues

**Port 3000 Already in Use**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

**Module Not Found**
```bash
rm -rf node_modules package-lock.json
npm install
```

**API Not Connecting**
- Verify backend is running
- Check `REACT_APP_API_URL` in .env
- Check browser console for errors (F12)
- Verify CORS is enabled in backend

**Styles Not Loading**
```bash
npm run build
npm start
```

### Common Issues

**"Cannot connect to database"**
1. Verify MySQL service is running
2. Check credentials in .env
3. Create database: `CREATE DATABASE resume_screening_db;`
4. Restart backend server

**"ImportError: No module named..."**
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt`
3. Check Python version (3.8+)

**"Module '@module' not found" (Frontend)**
1. Delete `node_modules` folder
2. Delete `package-lock.json`
3. Run `npm install`

## Development Commands

### Backend

```bash
# Start development server
python app.py

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

### Frontend

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Production Deployment

See [Production Deployment Guide](./DEPLOYMENT.md) for:
- Docker containerization
- Cloud deployment (AWS, Heroku, Vercel)
- Performance optimization
- Security hardening

## Need Help?

1. Check [Backend README](./backend/README.md)
2. Check [Frontend README](./frontend/README.md)
3. Review [Main README](./README.md)
4. Check logs in `backend/logs/`
5. Review error messages in browser console (F12)

## Next Steps

After successful installation:

1. **Read Documentation**
   - Backend API docs
   - Frontend components guide
   - Database schema

2. **Explore Features**
   - Upload sample resumes
   - Create job descriptions
   - Test matching algorithm

3. **Customize**
   - Modify scoring weights in `ranking.py`
   - Adjust AI prompts in `ai_agent.py`
   - Customize UI in React components

4. **Deploy**
   - Set up production environment
   - Configure SSL/TLS
   - Set up CI/CD pipeline

---

Happy building! 🚀
>>>>>>> 279d581c598bb782b6b22e7e1e3ab44043e32b29
