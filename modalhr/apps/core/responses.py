# apps/core/responses.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


def success_response(data=None, message="Success", http_status=status.HTTP_200_OK):
    """
    Standard success response.
    Returns:
        Response: {"success": True, "message": message, "data": data}
    """
    return Response({
        'success': True,
        'message': message,
        'data': data
    }, status=http_status)


def error_response(message="Error", errors=None, http_status=status.HTTP_400_BAD_REQUEST):
    """
    Standard error response.
    Returns:
        Response: {"success": False, "message": message, "errors": errors}
    """
    return Response({
        'success': False,
        'message': message,
        'errors': errors or {}
    }, status=http_status)


def paginated_response(queryset, serializer_class, request, view=None):
    """
    Handles pagination for a DRF ViewSet.
    Arguments:
        queryset (QuerySet): The queryset to paginate.
        serializer_class (Serializer): DRF serializer for the objects.
        request (Request): DRF request object.
        view (GenericAPIView, optional): DRF view instance for pagination context.
    Returns:
        Response: Paginated standard response structure.
    """
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request, view=view)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    # No pagination needed
    serializer = serializer_class(queryset, many=True)
    return success_response(serializer.data)
