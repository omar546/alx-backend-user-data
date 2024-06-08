#!/usr/bin/env python3
"""
Session Authentication Module
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Class to manage session authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session ID for a given user ID.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: The newly created session ID or None if the user_id is invalid.
        """

        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on the provided session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID or None if not found.
        """

        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session cookie in the request.

        Args:
            request: The Flask request object containing the session cookie.

        Returns:
            User: The User object corresponding to the session ID, or None if not found.
        """

        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the current session based on the session cookie in the request.

        Args:
            request: The Flask request object containing the session cookie.

        Returns:
            bool: True if the session was successfully deleted, False otherwise.
        """

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        if not self.user_id_for_session_id(session_cookie):
            return False
        del self.user_id_by_session_id[session_cookie]

        return True
