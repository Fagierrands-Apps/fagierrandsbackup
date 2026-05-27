from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.core.cache import cache
import logging
import traceback

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """Block IPs making excessive requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_requests = 100  # per minute
        self.block_duration = 3600  # 1 hour
    
    def __call__(self, request):
        ip = self.get_client_ip(request)
        
        # Check if IP is blocked
        if cache.get(f'blocked_{ip}'):
            logger.warning(f"Blocked IP attempted access: {ip}")
            return HttpResponseForbidden("Too many requests. Try again later.")
        
        # Count requests
        cache_key = f'requests_{ip}'
        requests = cache.get(cache_key, 0)
        
        if requests > self.max_requests:
            cache.set(f'blocked_{ip}', True, self.block_duration)
            logger.error(f"IP blocked for excessive requests: {ip} ({requests} requests)")
            return HttpResponseForbidden("Rate limit exceeded. IP blocked for 1 hour.")
        
        # Increment counter
        cache.set(cache_key, requests + 1, 60)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip


class BlockInsecureMethodsMiddleware:
    """Block insecure HTTP methods"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method in ['TRACE', 'TRACK', 'DEBUG']:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return self.get_response(request)

class CorsMiddleware:
    """Custom CORS middleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = self.get_allowed_origin(request)
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Max-Age'] = '86400'
            return response
        
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = self.get_allowed_origin(request)
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    def get_allowed_origin(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin:
            return origin
        
        allowed_origins = [
            'https://fagierrands-x9ow.vercel.app',
            'https://fagierrands.vercel.app',
            'https://fagierrand.fagitone.com',
        ]
        
        if origin in allowed_origins:
            return origin
        
        if origin and origin.endswith('.vercel.app'):
            return origin
            
        return '*'


class SafeWSGIMiddleware:
    """Catch exceptions and prevent WSGI handler errors"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"WSGI error on {request.path}: {str(e)}")
            logger.error(traceback.format_exc())
            return HttpResponse("Internal Server Error", status=500)
