# Django Built-in modules
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import serializers

# Local Apps
from .roles import RoleSerializer
from ..models import UserRole

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with roles.
    """
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'roles')
        read_only_fields = ('id', 'username', 'date_joined', 'last_login', 'roles')

    def get_roles(self, obj):
        """
        Get active roles for the user.
        """
        user_roles = UserRole.objects.filter(user=obj, is_active=True).select_related('role')
        return RoleSerializer([ur.role for ur in user_roles], many=True).data


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

