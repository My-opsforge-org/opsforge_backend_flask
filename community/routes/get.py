from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.models import User
from community.models import Community

def register_routes(bp):
    @bp.route('/communities', methods=['GET'])
    @jwt_required()
    def get_communities():
        communities = Community.query.all()
        return jsonify([c.to_dict() for c in communities]), 200

    @bp.route('/communities/<int:community_id>', methods=['GET'])
    @jwt_required()
    def get_community(community_id):
        community = Community.query.get_or_404(community_id)
        return jsonify(community.to_dict(include_members=True)), 200

    @bp.route('/communities/joined', methods=['GET'])
    @jwt_required()
    def get_joined_communities():
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return jsonify([c.to_dict() for c in user.communities_joined]), 200 