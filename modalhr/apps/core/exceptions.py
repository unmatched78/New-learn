import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, PermissionDenied

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Wrap DRF and Django exceptions in a uniform JSON response:
    {
        "success": False,
        "message": "<summary>",
        "errors": <dict or list>,
        "data": None
    }
    """
    # Let DRF generate the standard response, if it can
    response = drf_exception_handler(exc, context)

    # Handle Django ValidationError (forms/models)
    if isinstance(exc, DjangoValidationError):
        detail = exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
        response = Response(
            {
                'success': False,
                'message': 'Validation error',
                'errors': detail,
                'data': None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # If DRF handled it, normalize the payload
    elif response is not None:
        payload = {
            'success': False,
            'message': 'An error occurred',
            'errors': [],
            'data': None
        }

        if isinstance(response.data, dict):
            # Use `detail` if present as top‐level message
            if 'detail' in response.data:
                payload['message'] = response.data['detail']
            else:
                payload['errors'] = response.data
        elif isinstance(response.data, list):
            payload['errors'] = response.data
        else:
            payload['message'] = str(response.data)

        response.data = payload

    # Log everything
    logger.error(
        f"Exception in {context.get('view', 'unknown view')}: {exc}",
        exc_info=True
    )
    return response


# === Custom exceptions for your application ===

class ModuleNotActiveError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The requested module is not active for your tenant.'
    default_code = 'module_not_active'


class TenantNotFoundError(NotFound):
    default_detail = 'Tenant could not be determined or does not exist.'
    default_code = 'tenant_not_found'


class InsufficientPermissionError(PermissionDenied):
    default_detail = 'You do not have sufficient permission to perform this action.'
    default_code = 'insufficient_permission'


# You can add further domain-specific exceptions here, for example:

class ResourceConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'The request could not be completed due to a conflict with the current state of the target resource.'
    default_code = 'resource_conflict'

class ServiceUnavailableError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'The service is temporarily unavailable; please try again later.'
    default_code = 'service_unavailable'
