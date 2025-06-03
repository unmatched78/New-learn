from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Standardize error response format
        response.data = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail') or response.data,
                'details': response.data
            }
        }
    else:
        # Handle uncaught exceptions
        response = Response({
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal server error',
                'details': str(exc)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response