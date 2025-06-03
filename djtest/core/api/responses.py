# core/api/responses.py
from rest_framework.response import Response

def error_response(message, code=400, details=None):
    return Response({
        'error': {
            'code': code,
            'message': message,
            'details': details or {}
        }
    }, status=code)