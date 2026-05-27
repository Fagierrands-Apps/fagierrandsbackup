#!/usr/bin/env python
"""
Test Brevo email configuration
Run: python test_brevo_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("BREVO EMAIL CONFIGURATION TEST")
print("=" * 60)

print(f"\n📧 Email Settings:")
print(f"   Backend: {settings.EMAIL_BACKEND}")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   Port: {settings.EMAIL_PORT}")
print(f"   TLS: {settings.EMAIL_USE_TLS}")
print(f"   User: {settings.EMAIL_HOST_USER}")
print(f"   Password: {'***' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ ERROR: EMAIL_HOST_PASSWORD not set!")
    print("   Add to cPanel environment variables:")
    print("   EMAIL_HOST_PASSWORD=<your_brevo_smtp_key>")
    exit(1)

print("\n📤 Sending test email...")

try:
    send_mail(
        subject='Fagi Errands - Email Test',
        message='This is a test email from Fagi Errands backend.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@example.com'],  # Change to your email
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
    print("\n✅ Brevo configuration is working correctly")
    
except Exception as e:
    print(f"❌ Failed to send email: {str(e)}")
    print("\n🔍 Troubleshooting:")
    print("   1. Verify EMAIL_HOST_USER in cPanel")
    print("   2. Verify EMAIL_HOST_PASSWORD (SMTP key from Brevo)")
    print("   3. Check sender email is verified in Brevo")
    print("   4. Check Brevo account is active")
    exit(1)

print("=" * 60)
