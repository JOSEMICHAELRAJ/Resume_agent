# Resume Screening AI - Frontend

Modern React-based dashboard for the Resume Screening and Candidate Ranking System.

## Tech Stack

- **React 18** - UI framework
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Beautiful UI component library built on Tailwind
- **Recharts** - Charts and analytics
- **React Dropzone** - Drag-and-drop file uploads
- **React Hot Toast** - Toast notifications
- **Axios** - HTTP client
- **Lucide React** - Modern SVG icons

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   └── ...
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── UploadResumes.jsx
│   │   ├── CreateJob.jsx
│   │   ├── CandidateList.jsx
│   │   ├── JobList.jsx
│   │   ├── CandidateMatching.jsx
│   │   ├── RankingDetails.jsx
│   │   └── NotFound.jsx
│   ├── services/
│   │   └── api.js          # API service layer
│   ├── hooks/
│   │   └── useCustomHooks.js   # Custom React hooks
│   ├── utils/
│   │   └── helpers.js      # Utility functions
│   ├── App.jsx             # Main app component
│   ├── App.css
│   ├── index.js
│   └── index.css
├── .env                    # Environment variables
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS configuration
├── package.json
└── README.md              # This file
```

## Installation

### Prerequisites
- Node.js 14.0 or higher
- npm or yarn

### Steps

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Update .env with backend URL
   REACT_APP_API_URL=http://localhost:5000/api
   ```

3. **Start development server**
   ```bash
   npm start
   ```

   The application will open at `http://localhost:3000`

## Available Scripts

### `npm start`
Runs the app in development mode.
- Open [http://localhost:3000](http://localhost:3000) to view in browser
- The page will reload when you make changes

### `npm run build`
Builds the app for production to the `build` folder.
- Correctly bundles React in production mode
- Optimizes the build for the best performance

### `npm test`
Launches the test runner in interactive watch mode.

## Features

### Dashboard
- Overview statistics (total candidates, jobs, resumes)
- Quick action buttons
- Recent candidates list
- System health status

### Resume Upload
- Drag-and-drop file upload
- Support for PDF and DOCX formats
- Candidate information input
- Upload progress tracking
- Parsed skills display

### Job Management
- Create new job descriptions
- Extract skills from job descriptions
- View all jobs
- Match candidates to jobs

### Candidate Management
- List all candidates
- Search and filter candidates
- View candidate details
- Track resume uploads

### Candidate Matching
- Match candidates to job descriptions
- View ranking results
- Score breakdown visualization
- AI-generated candidate summaries
- Interview questions generation

### Ranking Details
- Detailed candidate-job matching analysis
- Score breakdown charts
- Skill matching analysis
- AI-generated summaries
- Interview questions
- Update recommendations (Shortlist/Pending/Reject)
- Export reports

## Components

### Navbar
- Application title and logo
- Connection status indicator
- User profile menu
- Navigation controls

### Sidebar
- Navigation menu
- Active route highlighting
- Mobile-responsive toggle
- Settings access

### Pages
All pages are responsive and include:
- Loading states
- Error handling
- Empty states
- Data validation

## API Service

The `api.js` service provides organized API calls:

```javascript
// Example usage
import { candidateAPI, jobAPI, resumeAPI } from '../services/api';

// Upload resume
const response = await resumeAPI.upload(file, candidateData);

// Get candidates
const candidates = await candidateAPI.list(page, perPage);

// Match candidates
const matches = await matchingAPI.matchCandidates(matchData);
```

## Custom Hooks

### useAsync
Handles async operations with loading, data, and error states.

### useFetch
Fetches data with automatic retry and refresh capabilities.

### useLocalStorage
Persists state to browser localStorage.

### useDebounce
Debounces value updates for search and filtering.

### useToast
Provides success, error, info, and loading notifications.

## Utility Functions

### Formatting
- `formatDate()` - Format dates consistently
- `formatTime()` - Format time values
- `formatFileSize()` - Display file sizes

### Styling
- `getScoreColor()` - Get text color based on score
- `getScoreBgColor()` - Get background color based on score
- `getRecommendationColor()` - Get badge color for recommendations

### Validation
- `isValidEmail()` - Validate email format
- `isValidPhone()` - Validate phone format

## Styling

The frontend uses:
- **Tailwind CSS** for utility-first styling
- **DaisyUI** for pre-built components
- **Custom CSS** for animations and overrides

### Color Scheme
- Primary Blue: `#3B82F6`
- Success Green: `#10B981`
- Warning Yellow: `#F59E0B`
- Error Red: `#EF4444`

## Environment Variables

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:5000/api

# Environment
REACT_APP_ENV=development
```

## Build and Deployment

### Build for Production
```bash
npm run build
```

Creates optimized production build in `build/` folder.

### Deploy to Hosting Services

**Vercel**
```bash
npm install -g vercel
vercel
```

**Netlify**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

**AWS S3 + CloudFront**
```bash
aws s3 sync build/ s3://your-bucket-name/
```

## Performance Optimization

- Code splitting with React.lazy()
- Image optimization
- CSS/JS minification
- Gzip compression
- Caching strategies
- Bundle size monitoring

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### API Connection Error
- Verify backend server is running on port 5000
- Check `REACT_APP_API_URL` in .env file
- Ensure CORS is enabled on backend

### Module Not Found
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 Already in Use
```bash
# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Styles Not Applying
```bash
# Rebuild Tailwind CSS
npm run build
```

## Performance Metrics

Target metrics:
- Lighthouse Score: > 90
- First Contentful Paint: < 2s
- Largest Contentful Paint: < 3s
- Cumulative Layout Shift: < 0.1

## Security

- XSS protection via React's built-in escaping
- CSRF tokens supported via API headers
- Secure HTTP-only cookie handling
- Input validation on client and server
- API rate limiting integration

## Future Enhancements

- Dark mode support
- Advanced analytics and charts
- Bulk candidate import
- Email integration
- Interview scheduling system
- PDF report generation
- Team collaboration features
- Interview recordings storage
- Candidate communication portal
- Advanced filtering and sorting

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License

## Support

For issues or questions, please:
1. Check the troubleshooting section
2. Review backend logs
3. Contact the development team

## Resources

- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [DaisyUI](https://daisyui.com)
- [Axios](https://axios-http.com)
- [React Router](https://reactrouter.com)
