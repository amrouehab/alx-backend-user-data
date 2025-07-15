#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path
        
        Args:
            path: The path to check
            excluded_paths: List of paths that don't require authentication
            
        Returns:
            True if authentication is required, False otherwise
        """
        if path is None:
            return True
        
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        # Make path slash tolerant
        if not path.endswith('/'):
            path += '/'
        
        # Check for wildcard patterns
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Remove the * and check if path starts with the prefix
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path == excluded_path:
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request
        
        Args:
            request: Flask request object
            
        Returns:
            The authorization header value or None
        """
        if request is None:
            return None
        
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request
        
        Args:
            request: Flask request object
            
        Returns:
            User object or None
        """
        return None
