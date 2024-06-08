#!/usr/bin/env python3
""" Authentication module for handling user authentication using Flask """

from flask import request
from typing import List, TypeVar
from models.user import User
from os import getenv


class Auth:
    """Class for user authentication methods"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication.

        Args:
            path (str): The URL path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if excluded_paths and path:
            if path[-1] == '/':
                path = path[:-1]
            else:
                path = path
            cleared_done = []
            for element in excluded_paths:
                if element[-1] == '/':
                    cleared_done.append(element[:-1])
                if element[-1] == '*':
                    if path.startswith(element[:-1]):
                        return False

            if path not in cleared_done:
                return True
            else:
                return False
        if path is None:
            return True
        if not excluded_paths:
            return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The Authorization header value if present, otherwise None.
        """
        if request is None:
            return None
        auth = request.headers.get('Authorization')
        if auth is None:
            return None
        else:
            return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user object if authenticated, otherwise None.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the request.
        Args:
        request: The Flask request object. If not provided, returns None.
        Returns:
        str: The value of the session cookie if it exists, otherwise None.
        """
        if request is None:
            return None
        cookie = getenv('SESSION_NAME')
        return request.cookies.get(cookie)
