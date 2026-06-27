"""
Comprehensive Request/Response Logging Middleware
Logs all API interactions, security events, and errors
"""
import logging
import json
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)
security_logger = logging.getLogger('security')
error_logger = logging.getLogger('error')


class ComprehensiveLoggingMiddleware(MiddlewareMixin):
    """
    Logs all requests, responses, and security events
    """
    
    def get_client_ip(self, request):
        """Get real client IP (handles proxies)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    def get_user_info(self, request):
        """Get user information"""
        if request.user and request.user.is_authenticated:
            return {
                'user_id': request.user.id,
                'username': request.user.username,
                'user_type': getattr(request.user, 'user_type', 'unknown')
            }
        return {'user_id': None, 'username': 'anonymous', 'user_type': 'anonymous'}
    
    def is_sensitive_endpoint(self, path):
        """Check if endpoint handles sensitive data"""
        sensitive_keywords = [
            'password', 'login', 'register', 'payment', 'token', 
            'admin', 'banking', 'verify', 'otp', 'reset'
        ]
        path_lower = path.lower()
        return any(keyword in path_lower for keyword in sensitive_keywords)
    
    def process_request(self, request):
        """Log incoming request"""
        request._start_time = time.time()
        
        ip = self.get_client_ip(request)
        user_info = self.get_user_info(request)
        path = request.path
        method = request.method
        
        # Log request
        log_data = {
            'type': 'REQUEST',
            'method': method,
            'path': path,
            'ip': ip,
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'user_type': user_info['user_type'],
            'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown')[:200],
            'query_params': dict(request.GET) if request.GET else None,
        }
        
        # Log body for POST/PUT/PATCH (excluding sensitive fields)
        if method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                body = json.loads(request.body) if request.body else {}
                # Mask sensitive fields
                safe_body = self.mask_sensitive_data(body)
                log_data['body'] = safe_body
            except:
                log_data['body'] = 'Unable to parse'
        
        # Check for potential security concerns
        if self.is_sensitive_endpoint(path):
            security_logger.warning(f"SENSITIVE_ENDPOINT | {json.dumps(log_data)}")
        else:
            logger.info(f"REQUEST | {json.dumps(log_data)}")
        
        return None
    
    def process_response(self, request, response):
        """Log response"""
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
        else:
            duration = 0
        
        ip = self.get_client_ip(request)
        user_info = self.get_user_info(request)
        
        log_data = {
            'type': 'RESPONSE',
            'method': request.method,
            'path': request.path,
            'ip': ip,
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'status': response.status_code,
            'duration_ms': round(duration * 1000, 2),
        }
        
        # Log response based on status code
        if response.status_code >= 500:
            error_logger.error(f"SERVER_ERROR | {json.dumps(log_data)}")
        elif response.status_code >= 400:
            security_logger.warning(f"CLIENT_ERROR | {json.dumps(log_data)}")
        elif response.status_code >= 300:
            logger.info(f"REDIRECT | {json.dumps(log_data)}")
        else:
            logger.info(f"SUCCESS | {json.dumps(log_data)}")
        
        return response
    
    def process_exception(self, request, exception):
        """Log exceptions"""
        ip = self.get_client_ip(request)
        user_info = self.get_user_info(request)
        
        log_data = {
            'type': 'EXCEPTION',
            'method': request.method,
            'path': request.path,
            'ip': ip,
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
        }
        
        error_logger.error(f"EXCEPTION | {json.dumps(log_data)}", exc_info=True)
        
        # Check for potential attack patterns
        if self.is_potential_attack(request, exception):
            security_logger.critical(f"POTENTIAL_ATTACK | {json.dumps(log_data)}")
        
        return None
    
    def mask_sensitive_data(self, data):
        """Mask sensitive data in logs"""
        if not isinstance(data, dict):
            return data
        
        sensitive_fields = [
            'password', 'token', 'secret', 'api_key', 'otp', 
            'pin', 'credit_card', 'cvv', 'ssn', 'national_id'
        ]
        
        masked_data = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in sensitive_fields):
                masked_data[key] = '***MASKED***'
            elif isinstance(value, dict):
                masked_data[key] = self.mask_sensitive_data(value)
            else:
                masked_data[key] = value
        
        return masked_data
    
    def is_potential_attack(self, request, exception):
        """Detect potential security attacks"""
        exception_str = str(exception).lower()
        attack_patterns = [
            'sql', 'injection', 'xss', 'script', 'exec', 
            'eval', '../', 'etc/passwd', 'union select',
            'drop table', 'base64', 'javascript:', 'onerror'
        ]
        
        # Check exception message
        if any(pattern in exception_str for pattern in attack_patterns):
            return True
        
        # Check request path
        path = request.path.lower()
        if any(pattern in path for pattern in attack_patterns):
            return True
        
        # Check query parameters
        for value in request.GET.values():
            if any(pattern in str(value).lower() for pattern in attack_patterns):
                return True
        
        return False
