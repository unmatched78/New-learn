from rest_framework.response import Response

def success_response(data=None, message="Success", status=200):
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status)

def error_response(message="Error", errors=None, status=400):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors or {}
    }, status=status)

def paginated_response(queryset, serializer_class, request, status=200):
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = serializer_class(queryset, many=True)
    return success_response(serializer.data, status=status)