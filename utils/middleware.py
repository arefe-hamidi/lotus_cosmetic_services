# Django Built-in modules
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPI(MiddlewareMixin):
    """
    Middleware to disable CSRF protection for API endpoints.
    This allows API requests to work without CSRF tokens.
    """
    def process_request(self, request):
        """
        Disable CSRF for API endpoints.
        """
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None

