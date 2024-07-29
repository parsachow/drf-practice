from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    # permissions.IsADminUser and has_permission checks if the user is Admin. They check if the request.user = user.is_staff
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        # check return to see if request is GET or if they have Admin permission
        return request.method == 'GET' or admin_permission
        