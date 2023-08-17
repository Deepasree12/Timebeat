from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name']  
    search_fields = ['email', 'name'] 





admin.site.register(User, CustomUserAdmin)
# Register your models here.
