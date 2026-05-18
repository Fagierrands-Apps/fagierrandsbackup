from django.http import HttpResponse, JsonResponse
from django.conf import settings

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
