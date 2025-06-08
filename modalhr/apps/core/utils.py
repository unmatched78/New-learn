# apps/core/utils.py
import hashlib
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.db import models

def generate_unique_code(prefix='', length=8):
    """Generate a unique code with optional prefix"""
    import uuid
    code = str(uuid.uuid4()).replace('-', '')[:length].upper()
    return f"{prefix}{code}" if prefix else code

def get_model_changes(old_instance, new_instance):
    """Get changes between two model instances"""
    if not old_instance or not new_instance:
        return {}
    
    old_dict = model_to_dict(old_instance)
    new_dict = model_to_dict(new_instance)
    
    changes = {}
    for field, new_value in new_dict.items():
        old_value = old_dict.get(field)
        if old_value != new_value:
            changes[field] = {
                'old': old_value,
                'new': new_value
            }
    
    return changes

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def serialize_for_json(obj):
    """Serialize object for JSON storage"""
    return json.dumps(obj, cls=DjangoJSONEncoder)

def paginate_queryset(queryset, page_size=20, page=1):
    """Paginate a queryset"""
    from django.core.paginator import Paginator
    
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    return {
        'results': list(page_obj),
        'pagination': {
            'page': page_obj.number,
            'pages': paginator.num_pages,
            'per_page': page_size,
            'total': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    }

def send_notification(user, title, message, notification_type='INFO', data=None):
    """Send notification to user"""
    from apps.core.models import Notification
    
    notification = Notification.objects.create(
        tenant=user.current_tenant,
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
        data=data or {},
        created_by=user
    )
    
    # Here you could add email, SMS, or push notification logic
    
    return notification