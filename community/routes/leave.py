from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from auth.models import User
from community.models import Community

def register_routes(bp):
    @bp.route('/communities/<int:community_id>/leave', methods=['POST'])
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