# Django Built-in modules
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import serializers

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

    def validate_username(self, value):
        """
        Validate that username is unique in the database.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_('این نام کاربری قبلاً استفاده شده است. لطفاً نام کاربری دیگری انتخاب کنید.'))
        return value

    def validate_email(self, value):
        """
        Validate that email is unique in the database.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('این ایمیل قبلاً استفاده شده است. لطفاً ایمیل دیگری وارد کنید.'))
        return value

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
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
            )
        except Exception as e:
            # Handle database integrity errors
            from django.db import IntegrityError
            if isinstance(e, IntegrityError):
                if 'username' in str(e).lower() or 'unique constraint' in str(e).lower():
                    raise serializers.ValidationError({
                        'username': _('این نام کاربری قبلاً استفاده شده است. لطفاً نام کاربری دیگری انتخاب کنید.')
                    })
                elif 'email' in str(e).lower():
                    raise serializers.ValidationError({
                        'email': _('این ایمیل قبلاً استفاده شده است. لطفاً ایمیل دیگری وارد کنید.')
                    })
            raise
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

