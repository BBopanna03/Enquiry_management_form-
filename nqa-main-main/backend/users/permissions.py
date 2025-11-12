from rest_framework.permissions import BasePermission

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        user_role = getattr(request.user.accesscontrol, 'role', None)

        # Admin has full access
        if user_role == 'admin':
            return True

        # POST allowed for counsellor
        if request.method == 'POST':
            return user_role in ['admin', 'counsellor']

        # PATCH/PUT allowed for admin, accounts, counsellor
        if request.method in ['PATCH', 'PUT']:
            return user_role in ['admin', 'accounts', 'counsellor','hr']

        # GET allowed for all four roles
        if request.method == 'GET':
            return user_role in ['admin', 'counsellor', 'accounts', 'hr']

        # DELETE only admin
        if request.method == 'DELETE':
            return user_role == 'admin'

        # Optional fallback
        required_roles = getattr(view, 'required_roles', [])
        return user_role in required_roles

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
