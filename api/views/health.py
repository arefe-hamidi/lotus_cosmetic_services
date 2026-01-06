# Third Party Packages
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local Apps
from utils.permissions import AllowAnyWithAPIKey, IsAuthenticatedWithAPIKey


@api_view(['GET'])
@permission_classes([AllowAnyWithAPIKey])
def health_check(request):
    """
    Public health check endpoint.
    """
    return Response({
        'status': 'success',
        'message': 'API is running',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedWithAPIKey])
def protected_endpoint(request):
    """
    Protected endpoint that requires JWT access token.
    """
    return Response({
        'status': 'success',
        'message': 'This is a protected endpoint',
        'user': request.user.username if request.user.is_authenticated else None
    }, status=status.HTTP_200_OK)

