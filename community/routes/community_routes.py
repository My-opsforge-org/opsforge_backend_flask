from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Community

community_routes_bp = Blueprint('community_routes', __name__)

@community_routes_bp.route('/communities', methods=['POST'])
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

@community_routes_bp.route('/communities', methods=['GET'])
@jwt_required()
def get_communities():
    communities = Community.query.all()
    return jsonify([c.to_dict() for c in communities]), 200

@community_routes_bp.route('/communities/<int:community_id>', methods=['GET'])
@jwt_required()
def get_community(community_id):
    user_id = get_jwt_identity()
    community = Community.query.get_or_404(community_id)
    
    # Get detailed member information
    member_details = []
    for member in community.members:
        member_details.append({
            'id': member.id,
            'name': member.name,
            'email': member.email
        })
    
    community_data = community.to_dict(include_members=True)
    community_data['members_details'] = member_details
    community_data['current_user_id'] = user_id
    community_data['is_member'] = community.is_member(user_id)
    
    return jsonify(community_data), 200

@community_routes_bp.route('/communities/<int:community_id>/join', methods=['POST'])
@jwt_required()
def join_community(community_id):
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    user = User.query.get_or_404(user_id)
    community = Community.query.get_or_404(community_id)
    if user in community.members:
        return jsonify({'message': 'Already a member'}), 200
    community.members.append(user)
    db.session.commit()
    return jsonify({'message': 'Joined community'}), 200

@community_routes_bp.route('/communities/<int:community_id>/leave', methods=['POST'])
@jwt_required()
def leave_community(community_id):
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    user = User.query.get_or_404(user_id)
    community = Community.query.get_or_404(community_id)
    if user not in community.members:
        return jsonify({'message': 'Not a member'}), 200
    community.members.remove(user)
    db.session.commit()
    return jsonify({'message': 'Left community'}), 200

@community_routes_bp.route('/communities/joined', methods=['GET'])
@jwt_required()
def get_joined_communities():
    user_id = get_jwt_identity()
    
    # Convert user_id to integer for comparison
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    
    user = User.query.get_or_404(user_id)
    return jsonify([c.to_dict() for c in user.communities_joined]), 200 