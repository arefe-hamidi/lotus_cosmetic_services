# Django Built-in modules
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import serializers

# Local Apps
from ..models import Role, UserRole


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Role model.
    """
    class Meta:
        model = Role
        fields = ('id', 'name', 'code', 'description', 'is_active')
        read_only_fields = ('id',)


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for UserRole model.
    """
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source='role',
        write_only=True,
        required=False
    )

    class Meta:
        model = UserRole
        fields = ('id', 'role', 'role_id', 'is_active', 'created')
        read_only_fields = ('id', 'created')

