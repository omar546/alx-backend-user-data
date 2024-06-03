#!/usr/bin/env python3
""" Authentication module for handling user authentication using Flask """

from flask import request
from typing import List, TypeVar
from models.user import User

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
            cleared_done = [ep[:-1] if ep[-1] == '/' else ep for ep in excluded_paths]
            
            for e in cleared_done:
                if e[-1] == '*' and path.startswith(e[:-1]):
                    return False

            return path not in cleared_done
        
        return path is None or not excluded_paths

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
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user object if authenticated, otherwise None.
        """
        return None
