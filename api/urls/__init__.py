# Django Built-in modules
from django.urls import path, include

# Local Apps
from . import  auth_urls, role_urls

app_name = 'api'

urlpatterns = [
  
    # Authentication endpoints
    path('auth/', include(auth_urls)),
    
    # Role Management endpoints
    path('', include(role_urls)),
]

