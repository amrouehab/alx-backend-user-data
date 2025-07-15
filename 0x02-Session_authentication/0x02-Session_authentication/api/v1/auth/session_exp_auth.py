#!/usr/bin/env python3
"""
Session authentication with expiration module
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session authentication with expiration
    """
    
    def __init__(self):
        """
        Initialize SessionExpAuth
        """
        super().__init__()
        try:
            session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (ValueError, TypeError):
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Create a session with expiration data
        
        Args:
            user_id: User ID to create session for
            
        Returns:
            Session ID string or None
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return User ID based on Session ID with expiration check
        
        Args:
            session_id: Session ID to look up
            
        Returns:
            User ID string or None
        """
        if session_id is None:
            return None
        
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        
        return session_dict.get("user_id")
