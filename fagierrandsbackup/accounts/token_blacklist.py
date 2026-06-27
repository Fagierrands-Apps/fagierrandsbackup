"""
JWT Token Blacklist Service
Revokes tokens on logout
"""
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import logging

logger = logging.getLogger(__name__)


def blacklist_token(token_str):
    """
    Add token to blacklist
    Token will be blocked until its natural expiry
    """
    try:
        # Decode token to get expiry
        token = AccessToken(token_str)
        jti = str(token['jti'])  # JWT ID
        exp = token['exp']  # Expiry timestamp
        
        # Calculate TTL (time until expiry)
        from datetime import datetime
        now = datetime.now().timestamp()
        ttl = int(exp - now)
        
        if ttl > 0:
            # Add to blacklist with TTL
            cache.set(f'blacklist_{jti}', True, ttl)
            logger.info(f"Token blacklisted: {jti[:8]}... (TTL: {ttl}s)")
            return True
        else:
            logger.warning(f"Token already expired: {jti[:8]}...")
            return False
            
    except Exception as e:
        logger.error(f"Token blacklist error: {e}")
        return False


def is_token_blacklisted(token_str):
    """
    Check if token is blacklisted
    """
    try:
        token = AccessToken(token_str)
        jti = str(token['jti'])
        
        is_blacklisted = cache.get(f'blacklist_{jti}', False)
        
        if is_blacklisted:
            logger.warning(f"Blacklisted token used: {jti[:8]}...")
        
        return is_blacklisted
        
    except Exception as e:
        logger.error(f"Token check error: {e}")
        return True  # Block invalid tokens


def blacklist_refresh_token(refresh_token_str):
    """
    Blacklist refresh token and its associated access tokens
    """
    try:
        refresh = RefreshToken(refresh_token_str)
        jti = str(refresh['jti'])
        exp = refresh['exp']
        
        from datetime import datetime
        now = datetime.now().timestamp()
        ttl = int(exp - now)
        
        if ttl > 0:
            cache.set(f'blacklist_{jti}', True, ttl)
            logger.info(f"Refresh token blacklisted: {jti[:8]}...")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Refresh token blacklist error: {e}")
        return False
