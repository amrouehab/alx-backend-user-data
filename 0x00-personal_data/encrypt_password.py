#!/usr/bin/env python3
"""
This module handles secure password hashing and verification.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with a salt.

    Args:
        password: The password string to hash.

    Returns:
        A salted, hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verify a password against a given hashed password.

    Args:
        hashed_password: The hashed password.
        password: The plaintext password to check.

    Returns:
        True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

