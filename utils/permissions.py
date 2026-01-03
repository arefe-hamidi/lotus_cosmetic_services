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

