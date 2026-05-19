"""
Real-time Error Monitoring Middleware
Sends live error notifications to admin - EVERY ERROR
"""
import logging
import traceback
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)

class LiveErrorMonitoringMiddleware:
    """
    Middleware to capture and send real-time error notifications
    NO RATE LIMITING - Every exception triggers an email
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Capture EVERY exception and send email alerts
        """
        try:
            error_type = type(exception).__name__
            error_message = str(exception)
            error_traceback = traceback.format_exc()
            
            user = getattr(request, 'user', None)
            user_info = f"{user.email} (ID: {user.id})" if user and user.is_authenticated else "Anonymous"
            
            error_report = f"""
🚨 LIVE ERROR ALERT - Fagierrands Backend
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
🔴 Error Type: {error_type}
📝 Message: {error_message}

👤 User: {user_info}
🌐 Path: {request.path}
🔧 Method: {request.method}
📍 IP: {self.get_client_ip(request)}

📊 Request Data:
GET: {dict(request.GET)}
POST: {self.sanitize_post_data(request.POST)}

🔍 Full Traceback:
{error_traceback}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            logger.error(f"Live Error: {error_type} - {error_message}")
            
            # Send to ALL admin emails
            self.send_error_email(error_report, error_type)
                
        except Exception as e:
            logger.error(f"Error in monitoring middleware: {e}")
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def sanitize_post_data(self, post_data):
        sanitized = dict(post_data)
        sensitive_keys = ['password', 'token', 'secret', 'key', 'api_key']
        for key in list(sanitized.keys()):
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = '***REDACTED***'
        return sanitized
    
    def send_error_email(self, error_report, error_type):
        try:
            admin_emails = settings.ADMIN_EMAILS
            
            send_mail(
                subject=f'🚨 Backend Error: {error_type}',
                message=error_report,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True,
            )
            logger.info(f"Error notification sent to {', '.join(admin_emails)}")
        except Exception as e:
            logger.error(f"Failed to send error email: {e}")

