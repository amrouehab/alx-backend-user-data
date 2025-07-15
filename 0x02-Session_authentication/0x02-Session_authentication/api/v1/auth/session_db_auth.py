#!/usr/bin/env python3
"""
Session authentication with database storage module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Session authentication with database storage
    """
    
    def create_session(self, user_id=None):
        """
        Create and store new instance of UserSession and return Session ID
        
        Args:
            user_id: User ID to create session for
            
        Returns:
            Session ID string or None
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return User ID by requesting UserSession in database based on session_id
        
        Args:
            session_id: Session ID to look up
            
        Returns:
            User ID string or None
        """
        if session_id is None:
            return None
        
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        
        if not user_sessions:
            return None
        
        user_session = user_sessions[0]
        
        # Check for expiration using parent class logic
        if self.session_duration <= 0:
            return user_session.user_id
        
        from datetime import datetime, timedelta
        if user_session.created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy UserSession based on Session ID from request cookie
        
        Args:
            request: Flask request object
            
        Returns:
            True if session destroyed, False otherwise
        """
        if request is None:
            return False
        
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        
        if not user_sessions:
            return False
        
        user_session = user_sessions[0]
        user_session.remove()
        return True
