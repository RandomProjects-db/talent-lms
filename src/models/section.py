from datetime import datetime
from src.models.user import db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), default='medium')  # 'critical', 'high', 'medium', 'low'
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('Item', backref='section', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Section {self.name}>'

    def to_dict(self, include_items=False):
        result = {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'priority': self.priority,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_items:
            # Get only top-level items (no parent)
            top_level_items = [item for item in self.items if item.parent_id is None]
            result['items'] = [item.to_dict(include_children=True) for item in sorted(top_level_items, key=lambda x: x.order_index)]
            
        return result

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)  # for child items
    text = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # 'critical', 'high', 'medium', 'low'
    type = db.Column(db.String(20), default='feature')  # 'feature', 'comment', 'ux-decision'
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship for hierarchical structure
    children = db.relationship('Item', backref=db.backref('parent', remote_side=[id]), lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Item {self.text[:50]}>'

    def to_dict(self, include_children=False):
        result = {
            'id': self.id,
            'section_id': self.section_id,
            'parent_id': self.parent_id,
            'text': self.text,
            'description': self.description,
            'priority': self.priority,
            'type': self.type,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_children and self.children:
            result['children'] = [child.to_dict(include_children=True) for child in sorted(self.children, key=lambda x: x.order_index)]
            
        return result

