from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.core.cache import cache
import logging
import traceback

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """Block IPs making excessive requests with endpoint-specific limits and progressive banning"""

    # (requests per minute, ban duration in seconds)
    LIMITS = {
        '/api/accounts/login/':          (3,  3600),   # 3/min → 1hr ban
        '/api/accounts/register/':       (5,  7200),   # 5/min → 2hr ban
        '/api/accounts/forgot-password/':(3,  3600),
        '/api/accounts/reset-password/': (3,  3600),
        '/api/accounts/verify-email/':   (5,  1800),
        '/api/orders/payment/':          (20, 1800),
        'default':                       (60, 3600),
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_limit(self, path):
        for endpoint, limits in self.LIMITS.items():
            if endpoint in path:
                return limits
        return self.LIMITS['default']

    def _get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', 'unknown')

    def __call__(self, request):
        ip = self._get_ip(request)
        path = request.path

        if cache.get(f'blocked_{ip}'):
            logger.warning(f"Blocked IP attempted access: {ip}")
            return HttpResponseForbidden("Too many requests. Try again later.")

        max_requests, ban_duration = self._get_limit(path)
        cache_key = f'rl_{ip}_{path}'
        count = cache.get(cache_key, 0)

        if count >= max_requests:
            # Progressive: each repeat offence doubles the ban
            offences = cache.get(f'offences_{ip}', 0) + 1
            cache.set(f'offences_{ip}', offences, 86400)
            duration = min(ban_duration * (2 ** (offences - 1)), 86400)  # cap at 24hr
            cache.set(f'blocked_{ip}', True, duration)
            logger.error(f"IP blocked: {ip} on {path} ({count} req, offence #{offences}, ban {duration}s)")
            return HttpResponseForbidden("Rate limit exceeded.")

        cache.set(cache_key, count + 1, 60)
        return self.get_response(request)


class BlockScannerMiddleware:
    """Block PHP shells, WordPress probes, scanner UAs, and known attack paths"""

    BLOCKED_EXTENSIONS = ('.php', '.asp', '.aspx', '.jsp', '.cgi', '.pl', '.sh')

    BLOCKED_PATH_PREFIXES = [
        '/wp-', '/wordpress', '/.env', '/.git', '/.htaccess',
        '/api/jolokia', '/phpmy', '/phpmyadmin', '/actuator',
        '/console', '/manager', '/cgi-bin', '/xmlrpc',
    ]

    BLOCKED_UA_KEYWORDS = [
        'masscan', 'zgrab', 'nmap', 'sqlmap', 'nikto', 'dirbuster',
        'nuclei', 'hydra', 'metasploit', 'python-requests/2.2', 'go-http-client/1.1',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower()
        ua = request.META.get('HTTP_USER_AGENT', '').lower()

        # Block PHP/script extension probes
        if any(path.endswith(ext) for ext in self.BLOCKED_EXTENSIONS):
            return HttpResponse(status=404)

        # Block known attack path prefixes
        if any(path.startswith(prefix) for prefix in self.BLOCKED_PATH_PREFIXES):
            return HttpResponse(status=404)

        # Block malicious user agents
        if any(kw in ua for kw in self.BLOCKED_UA_KEYWORDS):
            return HttpResponse(status=403)

        return self.get_response(request)


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
