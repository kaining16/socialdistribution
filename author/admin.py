from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    # 指定要在管理后台中显示的字段
    list_display = ('id', 'fqid', 'username', 'displayName', 'host', 'github', 'profileImage', 'page')

    # 搜索字段
    search_fields = ('username', 'displayName')

    # 可编辑的字段
    list_editable = ('displayName', 'host', 'github', 'profileImage', 'page')

    # 过滤器
    list_filter = ('host',)

    # 在管理后台的表单中显示的字段
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

# 注册 Author 模型
admin.site.register(Author, AuthorAdmin)