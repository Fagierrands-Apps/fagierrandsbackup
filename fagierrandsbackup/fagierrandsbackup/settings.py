import os
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# ENVIRONMENT VARIABLE VALIDATION
# ============================================
def validate_environment():
    """
    Validate that all critical environment variables are set.
    Raises ImproperlyConfigured if any required variable is missing.
    """
    required_vars = [
        'SECRET_KEY',
        'PG_DB_NAME',
        'PG_USER',
        'PG_PASSWORD',
        'PG_HOST',
        'SUPABASE_URL',
        'SUPABASE_SERVICE_ROLE_KEY',
        'EMAIL_HOST_PASSWORD',
    ]
    
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        raise ImproperlyConfigured(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Please set these variables in your cPanel Environment Variables table.\n"
            f"See env.example for the complete list of required variables."
        )

# Validate environment on startup
validate_environment()

# Optional: enable ORJSON renderer if installed
try:
    import rest_framework_orjson  # noqa: F401
    ORJSON_AVAILABLE = True
except Exception:
    ORJSON_AVAILABLE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [host.strip() for host in os.environ.get(
    'ALLOWED_HOSTS',
    'errandserver.fagitone.com,www.errandserver.fagitone.com,fagiserver.fagtone.com,fagierrand.fagitone.com,localhost,127.0.0.1,testserver'
).split(',')]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://fagierrands-server.onrender.com',
    'https://errandserver.fagitone.com',
    'https://www.errandserver.fagitone.com',
    'https://fagiserver.fagtone.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',  # Needed for Postgres-specific features (GIN/trigram)
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    # 'leaflet',  # Removed to avoid GDAL dependency
    # 'djgeojson',  # Removed to avoid GDAL dependency
    'channels',
    # Local apps
    'accounts',
    'orders',
    'locations',
    'notifications',
    'admin_dashboard',
    'voice',
    'marketplace',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Compress responses to reduce bandwidth
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'fagierrandsbackup.middleware.BlockInsecureMethodsMiddleware',  # Block TRACE/TRACK/DEBUG
    'fagierrandsbackup.middleware.CorsMiddleware',  # Our custom CORS middleware (first)
    'corsheaders.middleware.CorsMiddleware',  # Django CORS headers middleware (backup)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',  # ETag/Last-Modified handling
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fagierrandsbackup.error_monitoring.LiveErrorMonitoringMiddleware',  # Live error monitoring
]

# Use cookie-based sessions to avoid DB access in serverless
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# HTTPS Security - Enhanced
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'fagierrandsbackup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'orders/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fagierrandsbackup.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


#DATABASES = {
        #'default': {
            #'ENGINE': 'django.db.backends.sqlite3',
            #'NAME': BASE_DIR / 'db.sqlite3',
        #}
    #}

# Database configuration tuned for serverless environments to prevent connection exhaustion
# Prefer DATABASE_URL from environment; default to Supabase transaction pooler (6544)
import dj_database_url

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ['PG_DB_NAME'],
        "USER": os.environ['PG_USER'],
        "PASSWORD": os.environ['PG_PASSWORD'],
        "HOST": os.environ['PG_HOST'],
        "PORT": os.environ.get('PG_PORT', '5432'),
    },
}


# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Map Configuration (for frontend use)
MAP_CONFIG = {
    'DEFAULT_CENTER': (-1.2921, 36.8219),  # Nairobi coordinates
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        ['rest_framework_orjson.renderers.ORJSONRenderer']
        if ORJSON_AVAILABLE else ['rest_framework.renderers.JSONRenderer']
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,  # Changed to False to avoid dependency on a blacklist model
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS settings - PRODUCTION SECURE
CORS_ALLOW_ALL_ORIGINS = False  # Security: Only allow specific origins

# Explicitly allowed origins
CORS_ALLOWED_ORIGINS = [
    'https://fagierrands-x9ow.vercel.app',
    'https://fagierrands.vercel.app',
    'https://fagierrand.fagitone.com',
    'https://errandserver.fagitone.com',
    'https://www.errandserver.fagitone.com',
    'https://fagiserver.fagtone.com',
]

# For older browsers that don't support CORS_ALLOWED_ORIGINS
CORS_ORIGIN_WHITELIST = [
    'https://fagierrands-x9ow.vercel.app',
    'https://fagierrands.vercel.app',
    'https://fagierrand.fagitone.com',
    'https://errandserver.fagitone.com',
    'https://www.errandserver.fagitone.com',
    'https://fagiserver.fagtone.com',
]

# Allow requests from any subdomain of vercel.app
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://.*\.vercel\.app$",
]

CORS_ALLOW_CREDENTIALS = True  # Allow credentials (cookies, authorization headers)

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
    'pragma',
]

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
FILE_UPLOAD_PERMISSIONS = 0o644

# Additional CORS settings for preflight requests
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

# Supabase settings
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

# Media storage settings
MEDIA_STORAGE_BACKEND = os.environ.get('MEDIA_STORAGE_BACKEND', 'cloudinary')  # Options: cloudinary, mediafire, supabase, local

# Cloudinary settings
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')
CLOUDINARY_SECURE = os.environ.get('CLOUDINARY_SECURE', 'True') == 'True'
CLOUDINARY_UPLOAD_PRESET = os.environ.get('CLOUDINARY_UPLOAD_PRESET', '')  # Optional preset for unsigned uploads

# MediaFire Storage settings (legacy fallback)
# To get MediaFire API credentials:
# 1. Go to https://www.mediafire.com/developers/
# 2. Sign up for a developer account
# 3. Create a new application to get App ID and API Key
# 4. Set these environment variables in your .env file
MEDIAFIRE_APP_ID = os.environ.get('MEDIAFIRE_APP_ID', '')
MEDIAFIRE_API_KEY = os.environ.get('MEDIAFIRE_API_KEY', '')
MEDIAFIRE_EMAIL = os.environ.get('MEDIAFIRE_EMAIL', '')
MEDIAFIRE_PASSWORD = os.environ.get('MEDIAFIRE_PASSWORD', '')
MEDIAFIRE_FOLDER_KEY = os.environ.get('MEDIAFIRE_FOLDER_KEY', '')  # Optional: specific folder key

# GROQ AI API
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')

# Email settings - Using SMTP for email verification
# Configure for Brevo (free SMTP service) - 300 emails/day free
# To use Brevo: 
# 1. Sign up at https://www.brevo.com/
# 2. Go to SMTP & API > SMTP
# 3. Create SMTP key and set environment variables:
#    EMAIL_HOST_USER=your-brevo-email@example.com
#    EMAIL_HOST_PASSWORD=your-smtp-key

# SMTP Configuration for Real Email Sending - BREVO
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Brevo SMTP Settings (can be overridden via environment)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp-relay.brevo.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'

# SMTP Credentials (use environment in production)
# IMPORTANT: Update these with your actual Brevo credentials
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'smtp-relay.brevo.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # SECURITY: Must be set in environment

# Default sender address
# IMPORTANT: Ensure this email is verified in your Brevo account settings
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@fagitone.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Log email backend for development/debugging
if DEBUG:
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# Alternative: Use Gmail SMTP (if you prefer)
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'your-gmail@gmail.com'  
# EMAIL_HOST_PASSWORD = 'your-app-password'  # Generate from Google Account settings

# Frontend URL for email verification links
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://fagierrands-x9ow.vercel.app')

# Celery settings - disabled to work without Redis
# Using dummy URLs to prevent connection attempts
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'memory://')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'memory://')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks synchronously

# Web Push Notification settings
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')
WEBPUSH_EMAIL = os.environ.get('WEBPUSH_EMAIL', 'admin@fagierrands.com')

# Firebase Cloud Messaging settings
FCM_SERVER_KEY = os.environ.get('FCM_SERVER_KEY', '')

# NCBA Till API settings
BASE_URL = os.environ.get('BASE_URL', 'https://errandserver.fagitone.com')
NCBA_USERNAME = os.environ.get('NCBA_USERNAME', '').strip()
NCBA_PASSWORD = os.environ.get('NCBA_PASSWORD', '').strip()
NCBA_PAYBILL_NO = os.environ.get('NCBA_PAYBILL_NO', '').strip()
NCBA_TILL_NO = os.environ.get('NCBA_TILL_NO', '').strip()
NCBA_TRANSACTION_TYPE = os.environ.get('NCBA_TRANSACTION_TYPE', 'CustomerPayBillOnline').strip()
NCBA_USE_TILL_AS_ACCOUNT = os.environ.get('NCBA_USE_TILL_AS_ACCOUNT', 'False').strip().upper() == 'TRUE'
NCBA_CALLBACK_URL = f"{BASE_URL}/api/orders/payments/ncba/callback/"

# Legacy M-Pesa settings (maintained for backward compatibility)
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'production')
MPESA_CONSUMER_KEY = os.environ['MPESA_CONSUMER_KEY']
MPESA_CONSUMER_SECRET = os.environ['MPESA_CONSUMER_SECRET']
MPESA_SHORTCODE = os.environ['MPESA_SHORTCODE']
MPESA_PASSKEY = os.environ['MPESA_PASSKEY']
MPESA_PARTYB_SHORTCODE = os.environ['MPESA_PARTYB_SHORTCODE']

# Legacy M-Pesa Callback URLs
MPESA_STK_CALLBACK_URL = f"{BASE_URL}/api/orders/payments/mpesa/stk-callback/"
MPESA_C2B_VALIDATION_URL = f"{BASE_URL}/api/orders/payments/mpesa/c2b-validation/"
MPESA_C2B_CONFIRMATION_URL = f"{BASE_URL}/api/orders/payments/mpesa/c2b-confirmation/"
MPESA_B2C_RESULT_URL = f"{BASE_URL}/api/orders/payments/mpesa/b2c-result/"
MPESA_B2C_TIMEOUT_URL = f"{BASE_URL}/api/orders/payments/mpesa/b2c-timeout/"

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://fagierrands.com')


# Payment Processing Settings
# Configuration for automatic stuck payment handling
STUCK_PAYMENT_TIMEOUT_HOURS = int(os.environ.get('STUCK_PAYMENT_TIMEOUT_HOURS', '2'))
AUTO_FIX_STUCK_PAYMENTS = os.environ.get('AUTO_FIX_STUCK_PAYMENTS', 'True') == 'True'
STUCK_PAYMENT_NEW_STATUS = os.environ.get('STUCK_PAYMENT_NEW_STATUS', 'failed')  # Options: 'failed', 'cancelled', 'pending'

# Logging configuration for payment processing
# Enhanced logging with live email notifications - NO RATE LIMITING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'detailed': {
            'format': '{levelname} {asctime} {module} {funcName} {lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'email_admin': {
            'level': 'ERROR',
            'class': 'fagierrandsbackup.email_handler.LiveEmailHandler',
            'formatter': 'detailed',
        },
    },
    'root': {
        'handlers': ['console', 'email_admin'],
        'level': 'INFO',
    },
    'loggers': {
        'orders': {
            'handlers': ['console', 'email_admin'],
            'level': 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'email_admin'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Admin emails for error notifications (multiple recipients)
ADMIN_EMAILS = [
    'dallaherick0@gmail.com',
    'fagierrands1@gmail.com',
]


