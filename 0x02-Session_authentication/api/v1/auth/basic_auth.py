#!/usr/bin/env python3
"""
Basic Auth module for handling basic HTTP authentication
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii

class BasicAuth(Auth):
    """
    BasicAuth class for implementing Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 encoded part of the header if it exists, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        head_array = authorization_header.split(" ")
        if head_array[0] != "Basic":
            return None
        else:
            return head_array[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 encoded string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string if successful, otherwise None.
        """
        b64header = base64_authorization_header
        if b64header and isinstance(b64header, str):
            try:
                encode = b64header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            (str, str): The user email and password if they exist, otherwise (None, None).
        """
        decoded_b64 = decoded_base64_authorization_header
        if (decoded_b64 and isinstance(decoded_b64, str) and
                ":" in decoded_b64):
            res = decoded_b64.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the Authorization header.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The user object if authentication is successful, otherwise None.
        """

        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The user object if credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None
