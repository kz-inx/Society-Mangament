from django.contrib import admin
from .models import UserRole, UserPayMaintenance

# Register your models here.
admin.site.register(UserRole)
admin.site.register(UserPayMaintenance)
