#!/usr/bin/env python3
"""Module of User views for handling user-related API endpoints."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Return:
        - JSON response with a list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/<user_id>
    Path parameter:
        - user_id (str): ID of the User to retrieve.
    Return:
        - JSON response with the User object.
        - 404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/<user_id>
    Path parameter:
        - user_id (str): ID of the User to delete.
    Return:
        - JSON response with an empty dictionary if the User has been deleted.
        - 404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
        - email (str): User's email.
        - password (str): User's password.
        - last_name (str, optional): User's last name.
        - first_name (str, optional): User's first name.
    Return:
        - JSON response with the created User object.
        - 400 error if the User cannot be created.
    """
    response = None
    e_message = None
    try:
        response = request.get_json()
    except Exception as e:
        response = None
    if response is None:
        e_message = "Wrong format"
    if e_message is None and response.get("email", "") == "":
        e_message = "email missing"
    if e_message is None and response.get("password", "") == "":
        e_message = "password missing"
    if e_message is None:
        try:
            user = User()
            user.email = response.get("email")
            user.password = response.get("password")
            user.first_name = response.get("first_name")
            user.last_name = response.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            e_message = f"Can't create User: {e}"
    return jsonify({'error': e_message}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/<user_id>
    Path parameter:
        - user_id (str): ID of the User to update.
    JSON body:
        - last_name (str, optional): User's last name.
        - first_name (str, optional): User's first name.
    Return:
        - JSON response with the updated User object.
        - 404 error if the User ID doesn't exist.
        - 400 error if the User cannot be updated.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    response = None
    try:
        response = request.get_json()
    except Exception as e:
        response = None
    if response is None:
        return jsonify({'error': "Wrong format"}), 400
    if response.get('first_name') is not None:
        user.first_name = response.get('first_name')
    if response.get('last_name') is not None:
        user.last_name = response.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
