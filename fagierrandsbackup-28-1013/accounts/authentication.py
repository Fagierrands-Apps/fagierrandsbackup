"""
Custom JWT Authentication with blacklist support
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .token_blacklist import is_token_blacklisted


class BlacklistJWTAuthentication(JWTAuthentication):
    """
    JWT Authentication that checks token blacklist
    """
    
    def authenticate(self, request):
        # Get token from header
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        # Check if token is blacklisted
        if is_token_blacklisted(raw_token.decode('utf-8')):
            raise InvalidToken('Token has been revoked (logged out)')
        
        # Continue with normal authentication
        return super().authenticate(request)
