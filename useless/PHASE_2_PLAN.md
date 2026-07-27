# PHASE 2: Security & Stability Improvements

**Date:** May 27, 2026 10:36 AM  
**Priority:** HIGH  
**Estimated Time:** 2 hours

---

## ISSUES TO ADDRESS

From log analysis (stderr.log):
- **13,582 Unauthorized attempts** - Potential attack/abuse
- **7,217 Not Found errors** - Missing static files (Swagger UI)
- **30+ WSGI errors** - Request handling issues

---

## PHASE 2 BREAKDOWN

### Phase 2.1: Rate Limiting & Security (45 min)
**Priority:** CRITICAL  
**Impact:** Prevent API abuse, reduce server load

**Tasks:**
1. Add rate limiting middleware
2. Implement IP-based throttling
3. Add security headers
4. Block suspicious patterns

---

### Phase 2.2: Static Files Fix (15 min)
**Priority:** HIGH  
**Impact:** Fix 7,000+ 404 errors, working API docs

**Tasks:**
1. Run collectstatic
2. Configure WhiteNoise properly
3. Verify Swagger UI loads

---

### Phase 2.3: Error Handling (30 min)
**Priority:** MEDIUM  
**Impact:** Better error responses, logging

**Tasks:**
1. Add global exception handler
2. Improve WSGI error handling
3. Add request logging

---

### Phase 2.4: Monitoring & Health Checks (30 min)
**Priority:** MEDIUM  
**Impact:** Proactive issue detection

**Tasks:**
1. Add health check endpoint
2. Set up log rotation
3. Add performance monitoring

---

## PHASE 2.1: RATE LIMITING & SECURITY

### Issue Analysis:
```
13,582 Unauthorized attempts in logs:
- Pattern: Rapid requests to /api/accounts/profile/
- Pattern: Repeated /api/accounts/user/ calls
- Pattern: /api/locations/current/ spam
- Frequency: 3-5 requests per second
- Likely: Brute force or scraping attempt
```

### Solution: Multi-Layer Protection

#### 1. Enhanced Rate Limiting
```python
# File: fagierrandsbackup/settings.py

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/hour',          # Reduced from 100
        'user': '300/hour',         # Reduced from 1000
        'auth': '5/minute',         # New: Auth endpoints
        'payment': '10/hour',       # New: Payment endpoints
    }
}
```

#### 2. IP Blocking Middleware
```python
# File: fagierrandsbackup/middleware.py (new)

from django.http import HttpResponseForbidden
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """Block IPs making too many requests"""
    
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
            # Block IP
            cache.set(f'blocked_{ip}', True, self.block_duration)
            logger.error(f"IP blocked for excessive requests: {ip}")
            return HttpResponseForbidden("Rate limit exceeded. IP blocked.")
        
        # Increment counter
        cache.set(cache_key, requests + 1, 60)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

#### 3. Security Headers
```python
# File: fagierrandsbackup/settings.py

# Security Headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Additional security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
```

---

## PHASE 2.2: STATIC FILES FIX

### Issue:
```
7,217 Not Found errors:
- /static/drf-yasg/style.css
- /static/drf-yasg/swagger-ui-bundle.js
- /static/drf-yasg/swagger-ui.css
- /favicon.ico
```

### Solution:

#### 1. Collect Static Files
```bash
cd /home3/distinc3/fagiserver.fagtone.com
source virtualenv/fagiserver.fagtone.com/3.11/bin/activate
python manage.py collectstatic --noinput
```

#### 2. Verify WhiteNoise Configuration
```python
# File: fagierrandsbackup/settings.py (already configured)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Already present
    ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### 3. Add Favicon
```python
# File: fagierrandsbackup/urls.py

from django.views.generic import RedirectView

urlpatterns += [
    path('favicon.ico', RedirectView.as_view(
        url='/static/favicon.ico', 
        permanent=True
    )),
]
```

---

## PHASE 2.3: ERROR HANDLING

### Issue:
```
30+ WSGI errors:
[ERROR] wsgiAppHandler pApp->start_response() return NULL
```

### Solution:

#### 1. Global Exception Handler
```python
# File: fagierrandsbackup/middleware.py

class GlobalExceptionMiddleware:
    """Catch all unhandled exceptions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            return JsonResponse({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }, status=500)
```

#### 2. Request Logging
```python
# File: fagierrandsbackup/middleware.py

class RequestLoggingMiddleware:
    """Log all requests for monitoring"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(f"{request.method} {request.path} from {self.get_client_ip(request)}")
        
        response = self.get_response(request)
        
        # Log response status
        if response.status_code >= 400:
            logger.warning(f"{request.path} returned {response.status_code}")
        
        return response
```

---

## PHASE 2.4: MONITORING & HEALTH CHECKS

### 1. Health Check Endpoint
```python
# File: fagierrandsbackup/urls.py

from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """System health check endpoint"""
    checks = {
        'status': 'healthy',
        'database': check_database(),
        'cache': check_cache(),
        'timestamp': timezone.now().isoformat()
    }
    
    status_code = 200 if all([
        checks['database'], 
        checks['cache']
    ]) else 503
    
    return JsonResponse(checks, status=status_code)

def check_database():
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False

def check_cache():
    try:
        cache.set('health_check', 'ok', 10)
        return cache.get('health_check') == 'ok'
    except Exception:
        return False

urlpatterns += [
    path('health/', health_check, name='health-check'),
]
```

### 2. Log Rotation
```bash
# Add to cPanel cron jobs (daily at 2 AM):
0 2 * * * find /home3/distinc3/logs -name "*.log" -mtime +7 -delete
```

---

## EXECUTION PLAN

### Step 1: Rate Limiting (20 min)
- [ ] Update REST_FRAMEWORK settings
- [ ] Create middleware.py with rate limiting
- [ ] Add to MIDDLEWARE list
- [ ] Test with rapid requests

### Step 2: Static Files (10 min)
- [ ] Run collectstatic on server
- [ ] Add favicon redirect
- [ ] Test Swagger UI loads

### Step 3: Error Handling (15 min)
- [ ] Add exception middleware
- [ ] Add request logging
- [ ] Test error responses

### Step 4: Health Check (10 min)
- [ ] Add health check endpoint
- [ ] Test endpoint
- [ ] Set up monitoring

### Step 5: Testing (30 min)
- [ ] Test rate limiting works
- [ ] Verify static files load
- [ ] Check error handling
- [ ] Monitor logs

---

## EXPECTED IMPACT

### Before Phase 2:
- ❌ 13,582 unauthorized attempts (no protection)
- ❌ 7,217 static file 404s
- ❌ 30+ WSGI errors
- ❌ No monitoring
- ❌ Vulnerable to abuse

### After Phase 2:
- ✅ Rate limiting active (blocks abuse)
- ✅ Static files working (0 404s)
- ✅ Better error handling
- ✅ Health monitoring
- ✅ Protected against attacks

---

## RISK ASSESSMENT

**Risk Level:** LOW-MEDIUM  
**Breaking Changes:** None  
**Rollback:** Easy (remove middleware)  
**Testing Required:** YES (rate limiting)

---

## SUCCESS CRITERIA

- [ ] Rate limiting blocks excessive requests
- [ ] Static files load without 404s
- [ ] Swagger UI accessible
- [ ] Health check returns 200
- [ ] No WSGI errors in logs
- [ ] Unauthorized attempts reduced by 90%

---

**Ready to execute Phase 2.1 (Rate Limiting)?**
