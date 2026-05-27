from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import OTPVerification, User
import logging

logger = logging.getLogger(__name__)


def send_otp_email(user, request=None):
    """Send OTP verification email to user"""
    try:
        # Validate email configuration
        if not settings.EMAIL_HOST_PASSWORD:
            logger.error("EMAIL_HOST_PASSWORD not configured")
            return False, "Email service not configured. Contact administrator."
        
        # Delete existing unused OTPs
        OTPVerification.objects.filter(user=user, is_used=False).delete()
        
        # Create new OTP
        otp_verification = OTPVerification.objects.create(user=user)
        logger.info(f"Created OTP {otp_verification.otp_code} for {user.email}")
        
        # Email context
        context = {
            'user': user,
            'otp_code': otp_verification.otp_code,
            'expires_in_minutes': 10,
            'frontend_url': getattr(settings, 'FRONTEND_URL', 'https://fagierrands.com'),
        }
        
        # Render templates with fallback
        try:
            html_message = render_to_string('otp_verification.html', context)
            plain_message = render_to_string('otp_verification.txt', context)
        except Exception:
            plain_message = f"Your Fagi Errands verification code is: {otp_verification.otp_code}\n\nExpires in 10 minutes."
            html_message = f"<p>Your verification code: <strong>{otp_verification.otp_code}</strong></p><p>Expires in 10 minutes.</p>"
        
        # Send email
        send_mail(
            subject='Fagi Errands - Verification Code',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP sent to {user.email}")
        return True, "Verification code sent to your email"
        
    except Exception as e:
        logger.error(f"Failed to send OTP to {user.email}: {str(e)}")
        return False, f"Failed to send email: {str(e)}"


def verify_otp(email, otp_code):
    """Verify OTP code for email"""
    try:
        user = User.objects.filter(email=email).first()
        if not user:
            return False, "No user found with this email.", None
        
        otp_verification = OTPVerification.objects.filter(
            user=user, 
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp_verification:
            return False, "No valid OTP found. Request a new one.", None
        
        if otp_verification.is_expired():
            return False, "OTP expired. Request a new one.", None
        
        if otp_verification.is_max_attempts_reached():
            return False, "Max attempts reached. Request a new OTP.", None
        
        otp_verification.increment_attempts()
        
        if otp_verification.otp_code != otp_code:
            remaining = otp_verification.max_attempts - otp_verification.attempts
            if remaining > 0:
                return False, f"Invalid OTP. {remaining} attempts remaining.", None
            return False, "Invalid OTP. Max attempts reached.", None
        
        otp_verification.mark_as_used()
        user.is_email_verified = True
        user.save()
        
        logger.info(f"OTP verified for {user.email}")
        return True, "Email verified successfully", user
        
    except Exception as e:
        logger.error(f"OTP verification error: {str(e)}")
        return False, "Verification failed. Try again.", None


def resend_otp_email(email, request=None):
    """Resend OTP verification email"""
    try:
        user = User.objects.filter(email=email).first()
        if not user:
            return False, "No user found with this email."
        
        success, message = send_otp_email(user, request)
        return success, message
        
    except Exception as e:
        logger.error(f"Error resending OTP to {email}: {str(e)}")
        return False, "Failed to resend verification code."
