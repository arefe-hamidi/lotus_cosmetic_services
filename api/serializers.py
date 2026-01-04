# Django Built-in modules
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import serializers

# Local Apps
from .models import Role, UserRole

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        """
        Validate that password and password_confirm match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': _('رمز عبور و تأیید رمز عبور باید یکسان باشند.')
            })
        return attrs

    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


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


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        Validate that new_password and new_password_confirm match.
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': _('رمز عبور جدید و تأیید رمز عبور باید یکسان باشند.')
            })
        return attrs

    def validate_old_password(self, value):
        """
        Validate that old_password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('رمز عبور فعلی اشتباه است.'))
        return value

