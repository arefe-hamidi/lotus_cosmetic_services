# Django Built-in modules
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local Apps
from utils.permissions import HasRole
from ..models import Role, UserRole
from ..serializers import RoleSerializer, UserRoleSerializer

User = get_user_model()


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

