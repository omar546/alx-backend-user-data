#!/usr/bin/env python3
"""
Database module for managing user data with SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

# List of valid fields in the User model
VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

class DB:
    """
    DB class provides methods for interacting with the user database.
    """

    def __init__(self) -> None:
        """
        Initializes a new DB instance with a SQLite database.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        # Drop all tables and recreate them
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Creates and returns a memoized SQLAlchemy session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to User fields.

        Returns:
            User: The User object that matches the criteria.

        Raises:
            InvalidRequestError: If no valid fields are provided.
            NoResultFound: If no user matches the criteria.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the fields to update.

        Raises:
            ValueError: If any of the fields in kwargs are not valid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in VALID_FIELDS:
                raise ValueError
            setattr(user, k, v)
        session.commit()
