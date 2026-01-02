from django.shortcuts import redirect


class RedirectStaffMiddleware:
    """
    Middleware that redirects authenticated staff/superusers to the admin panel
    if they attempt to access any view that isn't part of the admin panel or logout.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that are EXEMPTED from redirect (Admin itself, logout, and static/media)
        exempt_paths = [
            "/admin/",
            "/users/logout/",
            "/users/api/logout/",
            "/static/",
            "/media/",
        ]

        if request.user.is_authenticated and request.user.is_staff:
            current_path = request.path

            # If the user is on a frontend page, redirect to admin
            is_exempt = any(current_path.startswith(path) for path in exempt_paths)

            if not is_exempt:
                return redirect("/admin/")

        response = self.get_response(request)
        return response
