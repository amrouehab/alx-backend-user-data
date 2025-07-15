#!/usr/bin/env python3
"""
Basic authentication module
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Basic authentication class
    """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract base64 part of Authorization header for Basic Authentication
        
        Args:
            authorization_header: Authorization header string
            
        Returns:
            Base64 part of Authorization header or None
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode base64 authorization header
        
        Args:
            base64_authorization_header: Base64 encoded string
            
        Returns:
            Decoded value as UTF8 string or None
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email and password from decoded base64 authorization header
        
        Args:
            decoded_base64_authorization_header: Decoded base64 string
            
        Returns:
            Tuple of (email, password) or (None, None)
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Return User instance based on email and password
        
        Args:
            user_email: User email
            user_pwd: User password
            
        Returns:
            User instance or None
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        
        if not users:
            return None
        
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve User instance for a request
        
        Args:
            request: Flask request object
            
        Returns:
            User instance or None
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)
