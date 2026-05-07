from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "role")
    search_fields = ("phone_number", "role", "user__username")
    list_filter = ("role",)