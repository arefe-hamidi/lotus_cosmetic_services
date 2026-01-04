# Third Party Packages
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AllowAnyWithAPIKey(BasePermission):
    """
    Allow access to anyone, but require API key validation.
    This permission class should be used for public endpoints.
    """
    def has_permission(self, request, view):
        # TODO: Implement API key validation logic
        # For now, allow all requests
        return True


class IsAuthenticatedWithAPIKey(BasePermission):
    """
    Allow access only to authenticated users with valid API key.
    This permission class should be used for protected endpoints.
    """
    def has_permission(self, request, view):
        # TODO: Implement API key validation logic
        # For now, check if user is authenticated
        return request.user and request.user.is_authenticated


class HasRole(BasePermission):
    """
    Permission class to check if user has a specific role.
    Usage: permission_classes = [HasRole('admin')]
    """
    def __init__(self, role_code):
        self.role_code = role_code

    def has_permission(self, request, view):
        """
        Check if user has the required role.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Import here to avoid circular imports
        from api.models import UserRole
        
        return UserRole.objects.filter(
            user=request.user,
            role__code=self.role_code,
            is_active=True,
            role__is_active=True
        ).exists()


class HasAnyRole(BasePermission):
    """
    Permission class to check if user has any of the specified roles.
    Usage: permission_classes = [HasAnyRole(['admin', 'staff'])]
    """
    def __init__(self, role_codes):
        self.role_codes = role_codes

    def has_permission(self, request, view):
        """
        Check if user has any of the required roles.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Import here to avoid circular imports
        from api.models import UserRole
        
        return UserRole.objects.filter(
            user=request.user,
            role__code__in=self.role_codes,
            is_active=True,
            role__is_active=True
        ).exists()

