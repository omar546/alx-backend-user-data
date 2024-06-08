#!/usr/bin/env python3
"""
Session Expiration class for managing session-based authentication with expiration.
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ 
    Session Expiration Authentication class that extends SessionAuth 
    to include session expiration functionality.
    """

    def __init__(self):
        """ 
        Initializes the SessionExpAuth class with session duration from environment variable. 
        """
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ 
        Creates a new session for a user and stores the creation timestamp.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: The session ID if the session is successfully created, otherwise None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_data = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ 
        Retrieves the user ID associated with a given session ID, considering session expiration.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if the session is valid and not expired, otherwise None.
        """

        if session_id is None:
            return None

        if session_id not in SessionAuth.user_id_by_session_id:
            return None

        session_data = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_data["user_id"]
        if "created_at" not in session_data:
            return None

        creation_time = session_data["created_at"]
        expiration_time = timedelta(seconds=self.session_duration)
        if (creation_time + expiration_time) < datetime.now():
            return None

        return session_data["user_id"]
