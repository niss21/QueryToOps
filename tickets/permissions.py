from rest_framework import permissions

class IsCreatorOrAssignee(permissions.BasePermission):
    """
    Custom permission to allow only the creator or assigned users to update the ticket.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by == request.user or
            request.user in obj.assigned_to.all()
        )
