from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models

# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=[
        'email',
    ]
    
    # Fields of the edit user page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ()
            }),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    
    #Fields of the create user page
    add_fieldsets = (
        (None,  {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.Profile, UserAdmin)