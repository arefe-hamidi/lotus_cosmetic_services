# Django Built-in modules
from django.contrib.auth import get_user_model

# Local Apps
from .authentication import (
    user_register,
    user_login,
    user_logout,
    UserProfileView,
    password_change,
)
from .health import (
    health_check,
    protected_endpoint,
)
from .roles import (
    RoleListViewSet,
    RoleDetailViewSet,
    user_role_list,
    user_role_remove,
)

User = get_user_model()

__all__ = [
    'health_check',
    'protected_endpoint',
    'user_register',
    'user_login',
    'user_logout',
    'UserProfileView',
    'password_change',
    'RoleListViewSet',
    'RoleDetailViewSet',
    'user_role_list',
    'user_role_remove',
]

