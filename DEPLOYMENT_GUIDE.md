# Pseudocode Editor - Deployment Guide

## 📁 Files You Need

Download the entire `pseudocode-editor` folder which contains:

```
pseudocode-editor/
├── src/
│   ├── models/
│   │   ├── user.py          # User authentication model
│   │   ├── project.py       # Project and team collaboration models
│   │   └── section.py       # Pseudocode sections and items models
│   ├── routes/
│   │   ├── user.py          # Authentication API endpoints
│   │   ├── project.py       # Project management API endpoints
│   │   └── section.py       # Pseudocode CRUD API endpoints
│   ├── static/
│   │   └── index.html       # Your beautiful dashboard (enhanced with backend integration)
│   ├── database/            # SQLite database folder (auto-created)
│   └── main.py              # Flask application entry point
├── requirements.txt         # Python dependencies
└── README.md               # Setup instructions
```

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Select your repository
   - Railway will auto-detect Flask and deploy!

3. **Environment Variables (set in Railway dashboard):**
   ```
   SECRET_KEY=your-secret-key-here-make-it-random
   ```

### Option 2: Render

1. **Push to GitHub** (same as above)

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Create new "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python src/main.py`

### Option 3: DigitalOcean App Platform

1. **Push to GitHub** (same as above)

2. **Deploy on DigitalOcean:**
   - Go to DigitalOcean App Platform
   - Create new app from GitHub
   - Select your repository
   - It will auto-detect the Flask app

## 🔧 Local Testing (Optional)

If you want to test locally first:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run the application
python src/main.py

# 3. Open browser to http://localhost:5000
```

## 🎯 What You Get

### Features Implemented:
- ✅ **User Authentication** - Register/Login system
- ✅ **Project Management** - Create and manage multiple projects
- ✅ **Team Collaboration** - Add team members to projects
- ✅ **Hierarchical Structure** - Sections with nested items
- ✅ **Priority System** - Critical, High, Medium, Low priorities
- ✅ **Item Types** - Features, Comments, UX Decisions
- ✅ **Search & Filter** - Find items quickly
- ✅ **Export Functionality** - Download project data as JSON
- ✅ **Responsive Design** - Works on desktop and mobile
- ✅ **Dark Theme** - Your original beautiful design preserved
- ✅ **Real-time Updates** - Changes persist in database

### Database:
- **SQLite** for development (auto-created)
- **PostgreSQL** for production (most hosting platforms provide this)

## 🔐 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CORS enabled for frontend-backend communication
- SQL injection protection via SQLAlchemy ORM

## 📊 Team Collaboration

- **Project Ownership** - Create and own projects
- **Member Management** - Add team members by username
- **Role-based Access** - Owner, Editor, Viewer roles
- **Shared Editing** - Multiple users can edit the same project

## 🛠 Customization

The application is built with:
- **Backend:** Flask + SQLAlchemy + SQLite
- **Frontend:** Your original HTML/CSS/JavaScript (enhanced)
- **Styling:** Preserved your beautiful dark theme
- **Icons:** Font Awesome (same as original)

## 📝 First Steps After Deployment

1. **Register your admin account** - First user becomes project owner
2. **Create your first project** - Import your existing pseudocode data
3. **Add team members** - Invite collaborators by username
4. **Start collaborating** - Everyone can edit in real-time

## 🔄 Data Migration

Your original pseudocode data structure is preserved. You can:
1. Export from the original HTML version
2. Import into the new system via the web interface
3. Or manually recreate (the structure is identical)

## 🆘 Support

If you need help:
1. Check the browser console for any JavaScript errors
2. Check server logs for backend issues
3. Ensure all environment variables are set correctly
4. Database will auto-create on first run

The application maintains your original design while adding powerful collaboration features!

