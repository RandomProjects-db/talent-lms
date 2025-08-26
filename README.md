# MIT Emerging Talent LMS - Interactive Pseudocode Editor

A collaborative pseudocode editor for learning and development, featuring hierarchical branching structure and real-time collaboration.

## Features

- 🔐 **User Authentication** - Secure login/register system
- 📋 **Project Management** - Create and manage multiple projects
- 🌳 **Hierarchical Structure** - Parent-child item relationships with side-by-side layout
- ✏️ **Interactive Editing** - Add, edit, delete items with modal forms
- 📊 **Priority System** - Critical, High, Medium, Low priority levels
- 🎯 **Item Types** - Feature, Bug, Comment, UX Decision categories
- 📤 **Export Functionality** - Download projects as JSON
- 📈 **Statistics** - View project statistics and metrics
- 🔍 **Search** - Find items across your pseudocode
- 🎨 **Modern UI** - Dark theme with professional styling

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with Font Awesome icons
- **Authentication**: Flask sessions

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Open http://localhost:5009

## Deployment

This application is configured for Railway deployment with automatic GitHub integration.

## Project Structure

```
├── main.py                 # Flask application entry point
├── src/
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   └── static/            # Frontend files
├── database/              # SQLite database
├── requirements.txt       # Python dependencies
└── Procfile              # Railway deployment config
```

## Usage

1. **Register/Login** to access the application
2. **Create a Project** for your pseudocode
3. **Add Sections** to organize your code structure
4. **Add Items** with parent-child relationships
5. **Use the side-by-side layout** to visualize branching logic
6. **Export** your projects for sharing or backup

## Contributing

This project is part of the MIT Emerging Talent program. Contributions and feedback are welcome!
