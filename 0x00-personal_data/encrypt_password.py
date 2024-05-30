#!/usr/bin/env python3
"""This module provides functions for hashing and validating passwords."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password and returns it as a byte string."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches the hashed password."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
