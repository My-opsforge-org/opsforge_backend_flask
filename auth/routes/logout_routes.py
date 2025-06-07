from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, timezone
from auth.models import db, TokenBlocklist
from . import auth_bp

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({'message': 'Successfully logged out'}), 200 