#!/usr/bin/env python3
"""
Module for session database authentication.
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing user sessions with database storage.
    """
    def create_session(self, user_id=None):
        """
        Create a new session for the given user ID.

        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            str: The generated session ID, or None if user_id is not provided.
        """
        session_id = super().create_session(user_id)
        if user_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID to lookup.

        Returns:
            str: The user ID associated with the session ID, or None if not found or expired.
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        session = sessions[0]
        start_time = session.created_at
        expiration_time = timedelta(seconds=self.session_duration)
        if (start_time + expiration_time) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the session associated with the request's session cookie.

        Args:
            request (Flask request object): The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        try:
            session.remove()
            UserSession.save_to_file()
        except Exception:
    
            return False

        return True
