#!/usr/bin/env python3
"""
User Module
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Base class for declarative class definitions
Base = declarative_base()


class User(Base):
    """
    User class represents a user entity in the database.
    """

    # Name of the table in the database
    __tablename__ = 'users'

    # Unique identifier for each user
    id = Column(Integer, primary_key=True)
    
    # Email address of the user (required)
    email = Column(String(250), nullable=False)
    
    # Hashed password of the user (required)
    hashed_password = Column(String(250), nullable=False)
    
    # Optional session ID for user session management
    session_id = Column(String(250), nullable=True)
    
    # Optional reset token for password recovery
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the User instance,
        displaying the user ID.
        """
        return f"User: id={self.id}"
