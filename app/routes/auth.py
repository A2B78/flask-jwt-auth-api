from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.role import Role
from app.schemas.user_schema import user_schema, user_schema_public
from app import db

bp = Blueprint('auth', __name__, url_prefix="/api/auth")

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 422

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400

    hashed_password = generate_password_hash(data['password'])
    role = Role.query.filter_by(name=data.get("role", "client")).first()

    new_user = User(
        username=data['username'],
        password=hashed_password,
        name=data['name'],
        email=data['email'],
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema_public.dump(new_user)), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Mauvais identifiants"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role.name})
    refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role.name})

    resp = jsonify({"msg": "Connexion réussie"})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity)
    resp = jsonify({"msg": "Token actualisé"})
    set_access_cookies(resp, new_token)
    return resp

@bp.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({"msg": "Déconnecté"})
    unset_jwt_cookies(resp)
    return resp