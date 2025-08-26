from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.project import Project, ProjectMember
from src.models.section import Section, Item

project_bp = Blueprint('project', __name__)

def require_auth():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return user_id

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get projects where user is owner or member
    projects = db.session.query(Project).join(ProjectMember).filter(
        ProjectMember.user_id == user_id
    ).all()
    
    # Return projects array directly (not wrapped in object)
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat()
    } for p in projects]), 200

@project_bp.route('/projects', methods=['POST'])
def create_project():
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Project name is required'}), 400
        
        # Create project
        project = Project(
            name=name,
            description=description,
            owner_id=user_id
        )
        
        db.session.add(project)
        db.session.flush()  # Get the project ID
        
        # Add owner as project member
        member = ProjectMember(
            project_id=project.id,
            user_id=user_id,
            role='owner'
        )
        
        db.session.add(member)
        db.session.commit()
        
        # Return project object directly
        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user has access to project
    member = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()
    
    if not member:
        return jsonify({'error': 'Access denied'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get sections with items
    sections = Section.query.filter_by(project_id=project_id).order_by(Section.order_index).all()
    
    sections_data = []
    for section in sections:
        items = Item.query.filter_by(section_id=section.id, parent_id=None).order_by(Item.order_index).all()
        
        def get_item_with_children(item):
            children = Item.query.filter_by(parent_id=item.id).order_by(Item.order_index).all()
            return {
                'id': item.id,
                'text': item.text,
                'description': item.description,
                'priority': item.priority,
                'type': item.type,
                'order_index': item.order_index,
                'children': [get_item_with_children(child) for child in children]
            }
        
        sections_data.append({
            'id': section.id,
            'name': section.name,
            'priority': section.priority,
            'order_index': section.order_index,
            'items': [get_item_with_children(item) for item in items]
        })
    
    # Return project data directly (not wrapped in object)
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'created_at': project.created_at.isoformat(),
        'updated_at': project.updated_at.isoformat(),
        'sections': sections_data
    }), 200

@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is owner
    member = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=user_id,
        role='owner'
    ).first()
    
    if not member:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.get_json()
        project.name = data.get('name', project.name)
        project.description = data.get('description', project.description)
        
        db.session.commit()
        
        # Return project object directly
        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'updated_at': project.updated_at.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is owner
    member = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=user_id,
        role='owner'
    ).first()
    
    if not member:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Delete all related data (cascade should handle this, but being explicit)
        sections = Section.query.filter_by(project_id=project_id).all()
        for section in sections:
            Item.query.filter_by(section_id=section.id).delete()
            db.session.delete(section)
        
        ProjectMember.query.filter_by(project_id=project_id).delete()
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
