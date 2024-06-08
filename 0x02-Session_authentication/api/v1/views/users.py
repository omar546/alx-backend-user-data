#!/usr/bin/env python3
"""
Module providing user-related API views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Retrieve a list of all users.

    Returns:
        - JSON list of all User objects
    """
    all_user = [user.to_json() for user in User.all()]
    return jsonify(all_user)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Retrieve a specific user by their ID.

    Path Parameter:
        - user_id (str): The ID of the user to retrieve.

    Returns:
        - JSON representation of the User object
        - 404 error if the User ID does not exist or is 'me' and the current user is not authenticated.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/<user_id>
    Delete a specific user by their ID.

    Path Parameter:
        - user_id (str): The ID of the user to delete.

    Returns:
        - Empty JSON response if the User has been correctly deleted
        - 404 error if the User ID does not exist
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
    """
    POST /api/v1/users/
    Create a new user.

    JSON Body:
        - email (str): The user's email address (required)
        - password (str): The user's password (required)
        - last_name (str): The user's last name (optional)
        - first_name (str): The user's first name (optional)

    Returns:
        - JSON representation of the newly created User object
        - 400 error if the User cannot be created
    """
    requestJSON_body = None
    error_msg = None
    try:
        requestJSON_body = request.get_json()
    except Exception as e:
        requestJSON_body = None
    if requestJSON_body is None:
        error_msg = "Wrong format"
    if error_msg is None and requestJSON_body.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and requestJSON_body.get("password", "") == "":
        error_msg = "password missing"


    if error_msg is None:
        try:
            user = User()
            user.email = requestJSON_body.get("email")
            user.password = requestJSON_body.get("password")
            user.first_name = requestJSON_body.get("first_name")
            user.last_name = requestJSON_body.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/<user_id>
    Update a user's information.

    Path Parameter:
        - user_id (str): The ID of the user to update.

    JSON Body:
        - last_name (str): The user's new last name (optional)
        - first_name (str): The user's new first name (optional)

    Returns:
        - JSON representation of the updated User object
        - 404 error if the User ID does not exist
        - 400 error if the User cannot be updated due to invalid input
    """

    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    requestJSON_body = None
    try:
        requestJSON_body = request.get_json()
    except Exception as e:
        requestJSON_body = None
    if requestJSON_body is None:
        return jsonify({'error': "Wrong format"}), 400
    if requestJSON_body.get('first_name') is not None:
        user.first_name = requestJSON_body.get('first_name')
    if requestJSON_body.get('last_name') is not None:
        user.last_name = requestJSON_body.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200

@app_views.route("/users/me", methods=['GET'], strict_slashes=False)
def get_authenticated_user():
    """
    GET /api/v1/users/me
    Retrieve the authenticated user's information.

    Returns:
        - JSON representation of the authenticated User object
        - 404 error if no user is currently authenticated
    """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_json())
