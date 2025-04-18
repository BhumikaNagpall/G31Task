from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser



class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'name', 'is_staff', 'is_superuser', 'phone')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name') 
    ordering = ('email',)


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),


    )


    # Fields visible when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone','password1', 'password2'),
        }),
    )
    def get_fieldsets(self, request, obj=None):
        if not obj:  # New user creation
            return self.add_fieldsets
        return self.fieldsets

    # Ensure we don't show 'username' in the admin when creating/editing a user
    def get_add_fieldsets(self, request, obj=None):
        return self.add_fieldsets

admin.site.register(AppUser, AppUserAdmin)
