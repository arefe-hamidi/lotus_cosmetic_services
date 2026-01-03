# Django Built-in modules
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

# Local Apps
from utils.permissions import AllowAnyWithAPIKey, IsAuthenticatedWithAPIKey
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
)

User = get_user_model()


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
@permission_classes([IsAuthenticatedWithAPIKey])
def protected_endpoint(request):
    """
    Protected endpoint that requires authentication.
    """
    return Response({
        'status': 'success',
        'message': 'This is a protected endpoint',
        'user': request.user.username if request.user.is_authenticated else None
    }, status=status.HTTP_200_OK)


# Authentication Views

@api_view(['POST'])
@permission_classes([AllowAnyWithAPIKey])
def user_register(request):
    """
    User registration endpoint.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'status': 'success',
            'message': _('کاربر با موفقیت ثبت نام شد.'),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAnyWithAPIKey])
def user_login(request):
    """
    User login endpoint.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    'status': 'success',
                    'message': _('ورود با موفقیت انجام شد.'),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': _('حساب کاربری غیرفعال است.')
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'status': 'error',
                'message': _('نام کاربری یا رمز عبور اشتباه است.')
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticatedWithAPIKey])
def user_logout(request):
    """
    User logout endpoint.
    """
    logout(request)
    return Response({
        'status': 'success',
        'message': _('خروج با موفقیت انجام شد.')
    }, status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateAPIView):
    """
    User profile view - GET and PUT endpoints.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedWithAPIKey]

    def get_object(self):
        """
        Return the current authenticated user.
        """
        return self.request.user

    def get_serializer_class(self):
        """
        Return appropriate serializer based on request method.
        """
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserProfileSerializer

    def update(self, request, *args, **kwargs):
        """
        Update user profile.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': _('پروفایل با موفقیت بروزرسانی شد.'),
            'user': UserProfileSerializer(instance).data
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedWithAPIKey])
def password_change(request):
    """
    Password change endpoint.
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({
            'status': 'success',
            'message': _('رمز عبور با موفقیت تغییر کرد.')
        }, status=status.HTTP_200_OK)
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

