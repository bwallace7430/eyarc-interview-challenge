from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "student_id") and request.student_id is not None
