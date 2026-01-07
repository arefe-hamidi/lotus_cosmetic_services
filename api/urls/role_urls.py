# Django Built-in modules
from django.urls import path

# Local Apps
from ..views import (
    RoleListViewSet,
    RoleDetailViewSet,
    user_role_list,
    user_role_remove,
)

urlpatterns = [
    # Role Management endpoints
    path('roles/', RoleListViewSet.as_view(), name='role_list'),
    path('roles/<int:pk>/', RoleDetailViewSet.as_view(), name='role_detail'),
    path('users/<int:user_id>/roles/', user_role_list, name='user_role_list'),
    path('users/<int:user_id>/roles/<int:role_id>/', user_role_remove, name='user_role_remove'),
]

