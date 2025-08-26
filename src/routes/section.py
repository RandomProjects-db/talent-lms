from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.project import ProjectMember
from src.models.section import Section, Item

section_bp = Blueprint('section', __name__)

def require_auth():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return user_id

def check_project_access(project_id, user_id):
    member = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()
    return member is not None

@section_bp.route('/projects/<int:project_id>/sections', methods=['POST'])
def create_section(project_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not check_project_access(project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        name = data.get('name')
        priority = data.get('priority', 'medium')
        
        if not name:
            return jsonify({'error': 'Section name is required'}), 400
        
        # Get next order index
        max_order = db.session.query(db.func.max(Section.order_index)).filter_by(project_id=project_id).scalar() or 0
        
        section = Section(
            project_id=project_id,
            name=name,
            priority=priority,
            order_index=max_order + 1
        )
        
        db.session.add(section)
        db.session.commit()
        
        return jsonify({
            'message': 'Section created successfully',
            'section': {
                'id': section.id,
                'name': section.name,
                'priority': section.priority,
                'order_index': section.order_index
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@section_bp.route('/sections/<int:section_id>/items', methods=['POST'])
def create_item(section_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check access through section's project
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    if not check_project_access(section.project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        text = data.get('text')
        description = data.get('description', '')
        priority = data.get('priority', 'medium')
        item_type = data.get('type', 'feature')
        parent_id = data.get('parent_id')
        
        if not text:
            return jsonify({'error': 'Item text is required'}), 400
        
        # Get next order index
        if parent_id:
            max_order = db.session.query(db.func.max(Item.order_index)).filter_by(
                section_id=section_id, parent_id=parent_id
            ).scalar() or 0
        else:
            max_order = db.session.query(db.func.max(Item.order_index)).filter_by(
                section_id=section_id, parent_id=None
            ).scalar() or 0
        
        item = Item(
            section_id=section_id,
            parent_id=parent_id,
            text=text,
            description=description,
            priority=priority,
            type=item_type,
            order_index=max_order + 1
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': {
                'id': item.id,
                'text': item.text,
                'description': item.description,
                'priority': item.priority,
                'type': item.type,
                'parent_id': item.parent_id,
                'order_index': item.order_index
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@section_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    section = Section.query.get(item.section_id)
    if not check_project_access(section.project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        item.text = data.get('text', item.text)
        item.description = data.get('description', item.description)
        item.priority = data.get('priority', item.priority)
        item.type = data.get('type', item.type)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': {
                'id': item.id,
                'text': item.text,
                'description': item.description,
                'priority': item.priority,
                'type': item.type,
                'parent_id': item.parent_id,
                'order_index': item.order_index
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@section_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    section = Section.query.get(item.section_id)
    if not check_project_access(section.project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Delete all child items recursively
        def delete_children(parent_id):
            children = Item.query.filter_by(parent_id=parent_id).all()
            for child in children:
                delete_children(child.id)
                db.session.delete(child)
        
        delete_children(item.id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@section_bp.route('/sections/<int:section_id>', methods=['PUT'])
def update_section(section_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    if not check_project_access(section.project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        section.name = data.get('name', section.name)
        section.priority = data.get('priority', section.priority)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Section updated successfully',
            'section': {
                'id': section.id,
                'name': section.name,
                'priority': section.priority,
                'order_index': section.order_index
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@section_bp.route('/sections/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    if not check_project_access(section.project_id, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Delete all items in section
        Item.query.filter_by(section_id=section_id).delete()
        db.session.delete(section)
        db.session.commit()
        
        return jsonify({'message': 'Section deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
