# Fix OTP to accept phone_number or email
with open('accounts/views.py', 'r') as f:
    content = f.read()

# Find SendOTPView post method and update it
old_code = '''    def post(self, request):
        """Send OTP verification email"""
        try:
            email = request.data.get('email')
            if not email:
                return Response({
                    'success': False,
                    'message': 'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST)'''

new_code = '''    def post(self, request):
        """Send OTP verification email"""
        try:
            email = request.data.get('email')
            phone_number = request.data.get('phone_number')
            
            if not email and not phone_number:
                return Response({
                    'success': False,
                    'message': 'Email or phone number is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # If phone provided, try to find user by phone
            if phone_number and not email:
                from .models import User
                try:
                    user = User.objects.get(phone_number=phone_number)
                    email = user.email
                except User.DoesNotExist:
                    return Response({
                        'success': False,
                        'message': 'User not found'
                    }, status=status.HTTP_400_BAD_REQUEST)'''

content = content.replace(old_code, new_code)

with open('accounts/views.py', 'w') as f:
    f.write(content)

print("✅ Fixed OTP to accept phone_number or email")
