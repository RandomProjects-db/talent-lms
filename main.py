import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Test deployment - data should persist with PostgreSQL!

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.project import Project, ProjectMember
from src.models.section import Section, Item
from src.routes.user import user_bp
from src.routes.project import project_bp
from src.routes.section import section_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(project_bp, url_prefix='/api')
app.register_blueprint(section_bp, url_prefix='/api')

# Database configuration
# Use PostgreSQL on Railway, SQLite locally
database_url = os.environ.get('DATABASE_URL')
print(f"🔍 DATABASE_URL: {database_url}")
print(f"🔍 RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT')}")

if database_url:
    # Railway PostgreSQL
    if database_url.startswith('postgres://'):
        # Fix for newer SQLAlchemy versions
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"✅ Using PostgreSQL: {database_url[:50]}...")
else:
    # Local SQLite fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    print("✅ Using SQLite fallback")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


@app.route('/test')
def test_login():
    return send_from_directory('.', 'test_login.html')

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5009))
    # Disable debug in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
