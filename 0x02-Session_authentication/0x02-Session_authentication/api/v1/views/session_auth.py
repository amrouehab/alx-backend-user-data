#!/usr/bin/env python3
"""
Module of Session Authentication views
"""
import os
from flask import abort, jsonify, request, make_response
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login
    Return:
      - User object JSON represented if login successful
      - Error messages for various failure cases
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    
    response = make_response(jsonify(user.to_json()))
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON dictionary if logout successful
      - 404 if session couldn't be destroyed
    """
    from api.v1.app import auth
    
    if not auth.destroy_session(request):
        abort(404)
    
    return jsonify({}), 200
