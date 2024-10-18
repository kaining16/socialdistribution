from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ('fqid', 'username', 'displayName', 'host', 'github', 'profileImage', 'page')

    
    search_fields = ('username', 'displayName')

    
    list_editable = ('displayName', 'host', 'github', 'profileImage', 'page')

    
    list_filter = ('host',)

    
    fieldsets = (
        (None, {
            'fields': ('fqid', 'username', 'displayName', 'host', 'github', 'profileImage', 'page')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
        ('Followers and Friends', {
            'fields': ('followers', 'friends'),
        }),
    )


admin.site.register(Author, AuthorAdmin)