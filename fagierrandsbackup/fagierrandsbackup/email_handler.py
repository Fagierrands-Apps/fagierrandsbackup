"""
Custom Email Handler for Critical Errors
Sends immediate email notifications for ERROR and CRITICAL logs
NO RATE LIMITING - Every error triggers an email
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

class LiveEmailHandler(logging.Handler):
    """
    Custom logging handler that sends emails for EVERY ERROR and CRITICAL log
    """
    def __init__(self):
        super().__init__()
        
    def emit(self, record):
        """
        Send email for EVERY error log
        """
        try:
            # Only send for ERROR and CRITICAL
            if record.levelno < logging.ERROR:
                return
            
            # Format the log message
            log_entry = self.format(record)
            
            # Create email body
            email_body = f"""
🚨 LIVE ERROR NOTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔴 Level: {record.levelname}
📦 Module: {record.module}
🔧 Function: {record.funcName}
📍 Line: {record.lineno}

📝 Message:
{record.getMessage()}

{log_entry}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Server: {settings.BASE_URL}
Environment: {'Production' if not settings.DEBUG else 'Development'}
"""
            
            # Send email to ALL admin emails
            admin_emails = settings.ADMIN_EMAILS  # Now a list
            
            send_mail(
                subject=f'🚨 {record.levelname}: {record.module} - {record.funcName}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True,
            )
            
        except Exception as e:
            # Don't let email failures break the application
            print(f"Failed to send error email: {e}")

