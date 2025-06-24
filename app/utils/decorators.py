from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User


def permission_required(permission_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.get(identity['id'])

            if not user or not user.has_permission(permission_name):
                return jsonify({"error": "Permission refusée"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper