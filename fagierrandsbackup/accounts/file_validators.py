"""
Secure file upload validation
Protects against malware, oversized files, and malicious uploads
"""
import os
import magic
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

# Allowed file types
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf'}
ALLOWED_ALL_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOCUMENT_EXTENSIONS

# File size limits
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

# MIME type whitelist
ALLOWED_IMAGE_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif'}
ALLOWED_DOCUMENT_MIMETYPES = {'application/pdf'}
ALLOWED_ALL_MIMETYPES = ALLOWED_IMAGE_MIMETYPES | ALLOWED_DOCUMENT_MIMETYPES


def validate_file_extension(filename):
    """Validate file has allowed extension"""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_ALL_EXTENSIONS:
        raise ValidationError(
            f'Invalid file type "{ext}". Allowed: {", ".join(ALLOWED_ALL_EXTENSIONS)}'
        )
    return ext


def validate_file_size(file, max_size=MAX_IMAGE_SIZE):
    """Validate file size"""
    if file.size > max_size:
        size_mb = max_size / (1024 * 1024)
        raise ValidationError(f'File too large. Maximum size: {size_mb}MB')


def validate_image_content(file):
    """Validate image file using magic bytes"""
    try:
        file.seek(0)
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        
        if mime not in ALLOWED_IMAGE_MIMETYPES:
            raise ValidationError(f'Invalid image type. Detected: {mime}')
        return True
    except Exception as e:
        logger.error(f'Image validation failed: {e}')
        raise ValidationError(f'Image validation failed: {str(e)}')


def validate_pdf_content(file):
    """Validate PDF file"""
    try:
        file.seek(0)
        header = file.read(4)
        file.seek(0)
        
        if header != b'%PDF':
            raise ValidationError('Invalid PDF file')
        
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        
        if mime not in ALLOWED_DOCUMENT_MIMETYPES:
            raise ValidationError(f'Invalid document type: {mime}')
        return True
    except Exception as e:
        logger.error(f'PDF validation failed: {e}')
        raise ValidationError(f'PDF validation failed: {str(e)}')


def sanitize_filename(filename):
    """Remove dangerous characters from filename"""
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    safe_name = os.path.basename(safe_name)
    return safe_name


def validate_upload(file, file_type='image'):
    """
    Comprehensive file validation
    
    Args:
        file: UploadedFile object
        file_type: 'image' or 'document'
    
    Returns:
        dict: {'valid': True, 'sanitized_name': str}
    
    Raises:
        ValidationError: If file is invalid or potentially malicious
    """
    if not file:
        raise ValidationError('No file provided')
    
    # 1. Validate extension
    ext = validate_file_extension(file.name)
    
    # 2. Validate size
    if file_type == 'image':
        validate_file_size(file, MAX_IMAGE_SIZE)
    else:
        validate_file_size(file, MAX_DOCUMENT_SIZE)
    
    # 3. Validate content (magic bytes)
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        validate_image_content(file)
    elif ext in ALLOWED_DOCUMENT_EXTENSIONS:
        validate_pdf_content(file)
    
    # 4. Sanitize filename
    safe_filename = sanitize_filename(file.name)
    
    # 5. Check for empty files
    if file.size == 0:
        raise ValidationError('Empty file not allowed')
    
    # 6. Check for null bytes (suspicious)
    file.seek(0)
    sample = file.read(1024)
    file.seek(0)
    if b'\x00' in sample and ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError('File contains suspicious content')
    
    logger.info(f'File validated: {safe_filename} ({file.size} bytes)')
    
    return {
        'valid': True,
        'sanitized_name': safe_filename,
        'extension': ext,
        'size': file.size
    }


# Django model field validators
def validate_image_upload(file):
    """Validator for ImageField"""
    try:
        validate_upload(file, file_type='image')
    except ValidationError as e:
        raise ValidationError(f'Image upload failed: {str(e)}')


def validate_document_upload(file):
    """Validator for FileField"""
    try:
        validate_upload(file, file_type='document')
    except ValidationError as e:
        raise ValidationError(f'Document upload failed: {str(e)}')
