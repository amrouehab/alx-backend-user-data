#!/usr/bin/env python3
"""
BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header
        
        Args:
            authorization_header: The authorization header string
            
        Returns:
            The Base64 part of the authorization header or None
        """
        if authorization_header is None:
            return None
        
        if not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 authorization header
        
        Args:
            base64_authorization_header: The Base64 encoded authorization header
            
        Returns:
            The decoded authorization header or None
        """
        if base64_authorization_header is None:
            return None
        
        if not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user credentials from decoded Base64 authorization header
        
        Args:
            decoded_base64_authorization_header: The decoded authorization header
            
        Returns:
            Tuple of (email, password) or (None, None)
        """
        if decoded_base64_authorization_header is None:
            return None, None
        
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        # Split only on first occurrence to allow passwords with ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Gets User instance based on email and password
        
        Args:
            user_email: The user's email
            user_pwd: The user's password
            
        Returns:
            User instance or None
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        
        if len(users) == 0:
            return None
        
        user = users[0]
        
        if not user.is_valid_password(user_pwd):
            return None
        
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request
        
        Args:
            request: Flask request object
            
        Returns:
            User instance or None
        """
        authorization_header = self.authorization_header(request)
        
        if authorization_header is None:
            return None
        
        base64_header = self.extract_base64_authorization_header(authorization_header)
        
        if base64_header is None:
            return None
        
        decoded_header = self.decode_base64_authorization_header(base64_header)
        
        if decoded_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)
