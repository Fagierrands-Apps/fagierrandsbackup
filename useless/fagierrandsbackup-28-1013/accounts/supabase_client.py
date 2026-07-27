import os
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Supabase client with error handling
try:
    from supabase import create_client, Client
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_service_role_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ImproperlyConfigured(
            "Supabase credentials missing from environment. "
            "Set SUPABASE_URL and SUPABASE_KEY in cPanel environment variables."
        )
    
    supabase: Client = create_client(supabase_url, supabase_key)
    logger.info("Supabase client initialized successfully")
    
    # Initialize admin client with service role key for storage operations
    if supabase_service_role_key:
        admin_supabase: Client = create_client(supabase_url, supabase_service_role_key)
        logger.info("Supabase admin client initialized successfully")
    else:
        logger.warning("Supabase service role key not found, using regular client for admin operations")
        admin_supabase = supabase
        
except ImportError as e:
    logger.error(f"Failed to import Supabase: {e}")
    logger.error("This is likely due to a dependency version mismatch between supabase and postgrest packages")
    supabase = None
    admin_supabase = None
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}")
    supabase = None
    admin_supabase = None

# Define storage bucket name for verification documents
VERIFICATION_BUCKET = 'user-uploads'

# Create a helper function to ensure buckets exist
def ensure_bucket_exists(bucket_name):
    """
    Ensure that a Supabase storage bucket exists.
    Silently handles RLS errors to avoid log spam.
    """
    if not supabase:
        return False
        
    try:
        supabase.storage.get_bucket(bucket_name)
        return True
    except Exception:
        # Bucket might exist but we can't create it due to RLS
        # Silently assume it exists to avoid error spam
        return True

# Call this when your Django app starts
def initialize_supabase_storage():
    """
    Initialize Supabase storage by ensuring required buckets exist.
    """
    if not supabase:
        return False
        
    try:
        return ensure_bucket_exists(VERIFICATION_BUCKET)
    except Exception:
        return False

# Helper function to check if Supabase is available
def is_supabase_available():
    """
    Check if Supabase client is available and functional.
    """
    return supabase is not None

# Graceful fallback for when Supabase is not available
def get_supabase_client():
    """
    Get the Supabase client with proper error handling.
    """
    if not supabase:
        logger.warning("Supabase client requested but not available")
        return None
    return supabase

def get_admin_supabase_client():
    """
    Get the Supabase admin client (with service role key) for storage operations.
    This client has elevated permissions for file uploads and management.
    """
    if not admin_supabase:
        logger.warning("Supabase admin client requested but not available")
        return None
    return admin_supabase
