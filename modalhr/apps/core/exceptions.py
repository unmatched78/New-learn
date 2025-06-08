# apps/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'An error occurred',
            'errors': [],
            'data': None
        }
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = response.data['detail']
            else:
                custom_response_data['errors'] = response.data
        elif isinstance(response.data, list):
            custom_response_data['errors'] = response.data
        else:
            custom_response_data['message'] = str(response.data)
        
        response.data = custom_response_data
    
    # Log the exception
    logger.error(f"Exception occurred: {exc}", exc_info=True)
    
    return response

class ModuleNotActiveError(Exception):
    """Exception raised when a module is not active for tenant"""
    pass

class TenantNotFoundError(Exception):
    """Exception raised when tenant is not found"""
    pass

class InsufficientPermissionError(Exception):
    """Exception raised when user doesn't have required permission"""
    pass