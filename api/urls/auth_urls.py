# Django Built-in modules
from django.urls import path

# Third Party Packages
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# Local Apps
from ..views import (
    user_register,
    user_login,
    user_logout,
    UserProfileView,
    password_change,
)

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('password/change/', password_change, name='password_change'),
    
    # JWT Token endpoints
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

