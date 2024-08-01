from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    # permissions.IsADminUser and has_permission checks if the user is Admin. They check if the request.user = user.is_staff
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        
        if request.method in permissions.SAFE_METHODS: #safe_methods = GET req and will return- True, if we want to grant permission for user to read object
            return True
        # if post, or other req is sent, check to see if logged in user == admin/staff
        else:
            return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        #check permissions for get/read only request
        if request.method in permissions.SAFE_METHODS: #safe_methods = GET req and will return- True, if we want to grant permission for user to read object
            return True
        
        #check permissions for post/put/delete request
        else:
            return obj.review_user == request.user or request.user.is_staff #checking to see if the person who wrote the review is the current logged in user or admin