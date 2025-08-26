# Backend Architecture Design for Pseudocode Editor

## Overview
Convert the HTML-based pseudocode editor into a persistent, collaborative web application using Flask backend with SQLite database and real-time updates.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (id)
);
```

### Project Members Table (for collaboration)
```sql
CREATE TABLE project_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role VARCHAR(20) DEFAULT 'member', -- 'owner', 'editor', 'viewer'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(project_id, user_id)
);
```

### Sections Table
```sql
CREATE TABLE sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    priority VARCHAR(20) DEFAULT 'medium',
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

### Items Table (hierarchical structure)
```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    parent_id INTEGER NULL, -- for child items
    text TEXT NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium', -- 'critical', 'high', 'medium', 'low'
    type VARCHAR(20) DEFAULT 'feature', -- 'feature', 'comment', 'ux-decision'
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections (id),
    FOREIGN KEY (parent_id) REFERENCES items (id)
);
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Projects
- `GET /api/projects` - Get user's projects
- `POST /api/projects` - Create new project
- `GET /api/projects/<id>` - Get project details
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Project Members
- `GET /api/projects/<id>/members` - Get project members
- `POST /api/projects/<id>/members` - Add member to project
- `DELETE /api/projects/<id>/members/<user_id>` - Remove member

### Sections
- `GET /api/projects/<id>/sections` - Get all sections for project
- `POST /api/projects/<id>/sections` - Create new section
- `PUT /api/sections/<id>` - Update section
- `DELETE /api/sections/<id>` - Delete section
- `PUT /api/sections/<id>/reorder` - Reorder sections

### Items
- `GET /api/sections/<id>/items` - Get all items for section
- `POST /api/sections/<id>/items` - Create new item
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item
- `PUT /api/items/<id>/reorder` - Reorder items

### Export/Import
- `GET /api/projects/<id>/export` - Export project as JSON
- `POST /api/projects/<id>/import` - Import project from JSON

## Real-time Collaboration Features

### WebSocket Events
- `item_created` - New item added
- `item_updated` - Item modified
- `item_deleted` - Item removed
- `section_created` - New section added
- `section_updated` - Section modified
- `section_deleted` - Section removed
- `user_joined` - User joined project
- `user_left` - User left project

### Implementation
- Use Flask-SocketIO for WebSocket support
- Broadcast changes to all project members
- Show live cursors/indicators of active users
- Conflict resolution for simultaneous edits

## Security Features

### Authentication
- JWT tokens for session management
- Password hashing with bcrypt
- Session timeout and refresh tokens

### Authorization
- Role-based access control (owner, editor, viewer)
- Project-level permissions
- API endpoint protection

### Data Validation
- Input sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

## Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-SocketIO** - WebSocket support for real-time features
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database (easily upgradeable to PostgreSQL)

### Frontend Integration
- Keep existing HTML/CSS/JavaScript structure
- Replace local storage with API calls
- Add WebSocket client for real-time updates
- Add authentication UI components

## Deployment Considerations

### Environment Variables
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - JWT signing key

### Production Features
- Database connection pooling
- Logging and monitoring
- Error handling and recovery
- Backup and restore procedures

## Migration Strategy

1. **Phase 1**: Create Flask backend with API endpoints
2. **Phase 2**: Modify frontend to use API instead of local storage
3. **Phase 3**: Add authentication and user management
4. **Phase 4**: Implement real-time collaboration features
5. **Phase 5**: Add advanced features (export/import, search, etc.)
6. **Phase 6**: Deploy and test with team

This architecture ensures scalability, maintainability, and provides a solid foundation for team collaboration while preserving the original design and functionality.

