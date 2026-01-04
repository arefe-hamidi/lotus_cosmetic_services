# Django Built-in modules
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local Apps
from utils.permissions import AllowAnyWithAPIKey, IsAuthenticatedWithAPIKey, HasRole, HasAnyRole
from .models import Role, UserRole
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    RoleSerializer,
    UserRoleSerializer,
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
    User login endpoint with JWT token generation.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Also create session for backward compatibility
                login(request, user)
                
                return Response({
                    'status': 'success',
                    'message': _('ورود با موفقیت انجام شد.'),
                    'tokens': {
                        'access': str(access_token),
                        'refresh': str(refresh),
                    },
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedWithAPIKey])
def user_logout(request):
    """
    User logout endpoint. Requires JWT access token.
    """
    logout(request)
    return Response({
        'status': 'success',
        'message': _('خروج با موفقیت انجام شد.')
    }, status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateAPIView):
    """
    User profile view - GET and PUT endpoints.
    Requires JWT access token for authentication.
    """
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedWithAPIKey])
def password_change(request):
    """
    Password change endpoint. Requires JWT access token.
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



# Role Management Views

class RoleListViewSet(ListCreateAPIView):
    """
    List and create roles. Requires admin role.
    """
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRole('admin')]

    def get_queryset(self):
        """
        Return active roles.
        """
        return Role.objects.filter(is_active=True).order_by('-created')


class RoleDetailViewSet(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a role. Requires admin role.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRole('admin')]

    def perform_destroy(self, instance):
        """
        Soft delete: set is_active to False instead of deleting.
        """
        instance.is_active = False
        instance.save()


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([HasRole('admin')])
def user_role_list(request, user_id):
    """
    List or add roles for a specific user. Requires admin role.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': _('کاربر یافت نشد.')
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_roles = UserRole.objects.filter(user=user, is_active=True).select_related('role')
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response({
            'status': 'success',
            'user': user.username,
            'roles': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            role_id = serializer.validated_data.get('role_id') or serializer.validated_data.get('role')
            if isinstance(role_id, Role):
                role = role_id
            else:
                try:
                    role = Role.objects.get(id=role_id, is_active=True)
                except Role.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': _('نقش یافت نشد.')
                    }, status=status.HTTP_404_NOT_FOUND)

            # Check if user already has this role
            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=role,
                defaults={'is_active': True}
            )
            
            if not created:
                user_role.is_active = True
                user_role.save()

            serializer = UserRoleSerializer(user_role)
            return Response({
                'status': 'success',
                'message': _('نقش با موفقیت به کاربر اضافه شد.'),
                'user_role': serializer.data
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([HasRole('admin')])
def user_role_remove(request, user_id, role_id):
    """
    Remove a role from a user. Requires admin role.
    """
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        user_role = UserRole.objects.get(user=user, role=role)
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': _('کاربر یافت نشد.')
        }, status=status.HTTP_404_NOT_FOUND)
    except Role.DoesNotExist:
        return Response({
            'status': 'error',
            'message': _('نقش یافت نشد.')
        }, status=status.HTTP_404_NOT_FOUND)
    except UserRole.DoesNotExist:
        return Response({
            'status': 'error',
            'message': _('این نقش به کاربر اختصاص داده نشده است.')
        }, status=status.HTTP_404_NOT_FOUND)

    user_role.is_active = False
    user_role.save()

    return Response({
        'status': 'success',
        'message': _('نقش با موفقیت از کاربر حذف شد.')
    }, status=status.HTTP_200_OK)
