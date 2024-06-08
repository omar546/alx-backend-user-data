#!/usr/bin/env python3
"""
Module providing index views for the API.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def get_status() -> str:
    """
    GET /api/v1/status
    Retrieve the status of the API.

    Returns:
        - JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def get_stats() -> str:
    """
    GET /api/v1/stats
    Retrieve the count of each type of object.

    Returns:
        - JSON response with the number of each object type.
    """
    from models.user import User
    statistics = {}
    statistics['users'] = User.count()
    return jsonify(statistics)


@app_views.route('/unauthorized', strict_slashes=False)
def handle_unauthorized() -> str:
    """
    GET /api/v1/unauthorized
    Simulate an unauthorized access attempt.

    Returns:
        - Aborts with a 401 status code.
    """
    abort(401)


@app_views.route('/forbidden', strict_slashes=False)
def handle_forbidden() -> str:
    """
    GET /api/v1/forbidden
    Simulate a forbidden access attempt.

    Returns:
        - Aborts with a 403 status code.
    """
    abort(403)
