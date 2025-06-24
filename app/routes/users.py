from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.utils.decorators import permission_required

bp = Blueprint('users', __name__, url_prefix="/api/users")

@bp.route('/', methods=['GET'])
@jwt_required()
@permission_required("manage_users")
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
