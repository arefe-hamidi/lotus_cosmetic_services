# Django Built-in modules
from django.urls import path

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
]

