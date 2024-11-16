from django.contrib import admin

from .models import User

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type') 
    list_filter = ('user_type',) 
    search_fields = ('username', 'email') 
