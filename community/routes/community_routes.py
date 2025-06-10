from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Community

community_bp = Blueprint('community', __name__)

@community_bp.route('/communities', methods=['POST'])
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

@community_bp.route('/communities', methods=['GET'])
@jwt_required()
def get_communities():
    communities = Community.query.all()
    return jsonify([c.to_dict() for c in communities]), 200

@community_bp.route('/communities/<int:community_id>', methods=['GET'])
@jwt_required()
def get_community(community_id):
    community = Community.query.get_or_404(community_id)
    return jsonify(community.to_dict(include_members=True)), 200

@community_bp.route('/communities/<int:community_id>/join', methods=['POST'])
@jwt_required()
def join_community(community_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    community = Community.query.get_or_404(community_id)
    if user in community.members:
        return jsonify({'message': 'Already a member'}), 200
    community.members.append(user)
    db.session.commit()
    return jsonify({'message': 'Joined community'}), 200

@community_bp.route('/communities/<int:community_id>/leave', methods=['POST'])
@jwt_required()
def leave_community(community_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    community = Community.query.get_or_404(community_id)
    if user not in community.members:
        return jsonify({'message': 'Not a member'}), 200
    community.members.remove(user)
    db.session.commit()
    return jsonify({'message': 'Left community'}), 200

@community_bp.route('/communities/joined', methods=['GET'])
@jwt_required()
def get_joined_communities():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify([c.to_dict() for c in user.communities_joined]), 200 