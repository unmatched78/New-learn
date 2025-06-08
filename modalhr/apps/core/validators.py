# apps/core/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_phone_number(value):
    """Validate phone number format"""
    phone_regex = re.compile(r'^\+?1?\d{9,15})
    if not phone_regex.match(value):
        raise ValidationError(_('Invalid phone number format'))

def validate_file_extension(value):
    """Validate file extension"""
    from django.conf import settings
    
    allowed_extensions = getattr(settings, 'HRMIS_SETTINGS', {}).get('FILE_TYPES_ALLOWED', [])
    if allowed_extensions:
        extension = value.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise ValidationError(
                _('File extension "%(extension)s" is not allowed.'),
                params={'extension': extension}
            )

def validate_file_size(value):
    """Validate file size"""
    from django.conf import settings
    
    max_size = getattr(settings, 'HRMIS_SETTINGS', {}).get('MAX_FILE_SIZE', 5 * 1024 * 1024)
    if value.size > max_size:
        raise ValidationError(
            _('File size cannot exceed %(max_size)s MB.'),
            params={'max_size': max_size // (1024 * 1024)}
        )
