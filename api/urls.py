# Django Built-in modules
from django.urls import path

# Third Party Packages
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# Local Apps
from . import views

app_name = 'api'

urlpatterns = [
    # Health and Test endpoints
    path('health/', views.health_check, name='health_check'),
    path('protected/', views.protected_endpoint, name='protected_endpoint'),
    
    # Authentication endpoints
    path('auth/register/', views.user_register, name='user_register'),
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/logout/', views.user_logout, name='user_logout'),
    path('auth/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('auth/password/change/', views.password_change, name='password_change'),
    
    # JWT Token endpoints
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Role Management endpoints
    path('roles/', views.RoleListViewSet.as_view(), name='role_list'),
    path('roles/<int:pk>/', views.RoleDetailViewSet.as_view(), name='role_detail'),
    path('users/<int:user_id>/roles/', views.user_role_list, name='user_role_list'),
    path('users/<int:user_id>/roles/<int:role_id>/', views.user_role_remove, name='user_role_remove'),
]

