from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from community.models import Community

def register_routes(bp):
    @bp.route('/communities', methods=['POST'])
    @jwt_required()
    def create_community():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        if Community.query.filter_by(name=name).first():
            return jsonify({'error': 'Community name already exists'}), 400
        community = Community(name=name, description=description)
        db.session.add(community)
        db.session.commit()
        return jsonify({'message': 'Community created', 'community': community.to_dict()}), 201 