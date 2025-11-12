# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AccessControl

# Define an inline admin descriptor for AccessControl model
class AccessControlInline(admin.StackedInline):
    model = AccessControl
    can_delete = False
    verbose_name_plural = 'Access Control'
    fields = ('role',)

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccessControlInline,)
    list_display = ('username', 'email', 'get_role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'accesscontrol__role')
    search_fields = ('username', 'email')

    def get_role(self, obj):
        try:
            return obj.accesscontrol.role
        except AccessControl.DoesNotExist:
            return "No Role Assigned"
    get_role.short_description = 'Role'

# Re-register User model with custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register AccessControl model separately for direct management
@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'role')