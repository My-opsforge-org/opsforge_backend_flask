from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Community

def register_routes(bp):
    @bp.route('/communities/<int:community_id>/join', methods=['POST'])
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