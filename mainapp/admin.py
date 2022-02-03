from django.contrib import admin
from .models import *
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'organization', 'customer',
#                     'organization_admin', 'is_active', 'created')
#     list_display_links = ('id', 'username', )
#     list_filter = ('is_active', 'created', )
#     list_editable = ('is_active', 'organization', 'customer', 'organization_admin',)
#     search_fields = ('username', 'mobile', 'is_active', 'created',)
#     date_hierarchy = 'created'
#     ordering = ('-created',)


admin.site.register(User)

# , UserAdmin