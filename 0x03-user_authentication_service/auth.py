#!/usr/bin/env python3
"""
Password Hashing and Authentication Module
"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import TypeVar

def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: A new UUID.
    """
    return str(uuid4())

class Auth:
    """Auth class to handle user authentication and session management"""

    def __init__(self):
        """
        Initializes the Auth instance with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Retrieves the user's email using the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user's email address, or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the user's session.

        Args:
            user_id (int): The user's ID.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the user's password using the reset token.

        Args:
            reset_token (str): The password reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
