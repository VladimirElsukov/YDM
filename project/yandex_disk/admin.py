from django.contrib import admin
from .models import File, UserProfile


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "modified_date", "mime_type")
    search_fields = ("name", "mime_type")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "registration_date")
    search_fields = ("name", "email")
