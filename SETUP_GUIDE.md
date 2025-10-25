# TaelioAI Setup Guide 🚀

This guide will help you run the TaelioAI system with both backend and frontend components.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Google Gemini API Key** (for AI functionality)

## Step 1: Backend Setup

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Set Up Environment Variables
Create a `.env` file in the `backend` directory:
```bash
# Create .env file
touch .env  # macOS/Linux
# or create manually on Windows
```

Add your Google Gemini API key to the `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**To get a Gemini API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste it into your `.env` file

### 1.5 Run the Backend Server
```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

**Test the backend:**
- Visit `http://localhost:8000` - should show API welcome message
- Visit `http://localhost:8000/docs` - FastAPI documentation

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Run the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173` (or another port if 5173 is busy)

## Step 3: Using the Application

1. **Open your browser** and go to `http://localhost:5173`
2. **Fill out the story form** with:
   - Story Title
   - Genre (select from dropdown)
   - Story Outline
3. **Click "Generate Story"** and wait for the AI to create your story
4. **View, copy, download, or print** your generated story

## API Endpoints

The backend provides these endpoints:

- `GET /` - API status
- `GET /health` - Health check
- `POST /story/write-story` - Generate a story
  - **Request Body:**
    ```json
    {
      "title": "Your Story Title",
      "genre": "Fantasy",
      "outline": "Your story outline..."
    }
    ```
  - **Response:**
    ```json
    {
      "story": "Generated story content..."
    }
    ```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Missing API Key Error:**
- Ensure your `.env` file is in the `backend` directory
- Check that `GEMINI_API_KEY` is set correctly
- Restart the backend server after adding the API key

### Frontend Issues

**Port 5173 already in use:**
- Vite will automatically use the next available port
- Check the terminal output for the actual URL

**Dependencies not installing:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Connection Issues

**Frontend can't connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check that CORS is properly configured (already set up)
- Verify the API URL in the frontend code matches your backend URL

## Development Tips

### Backend Development
- The backend uses FastAPI with auto-reload enabled
- API documentation is available at `http://localhost:8000/docs`
- Logs are displayed in the terminal

### Frontend Development
- Uses Vite for fast development
- Hot reload is enabled for instant updates
- Tailwind CSS is configured for styling

## Production Deployment

For production deployment, you'll need to:

1. **Backend:**
   - Use a production ASGI server like Gunicorn
   - Set up proper environment variables
   - Configure CORS for your domain

2. **Frontend:**
   - Build the production version: `npm run build`
   - Serve the `dist` folder with a web server
   - Update API URLs to point to production backend

## Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify all dependencies are installed
3. Ensure the API key is valid and has proper permissions
4. Check that both servers are running on the correct ports

Happy storytelling with TaelioAI! 📚✨

