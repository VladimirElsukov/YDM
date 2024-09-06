from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("oauth/callback/", views.oauth_callback, name="oauth_callback"),
    path("user_info/", views.user_info, name="user_info"),
    path("disk_files/", views.disk_files, name="disk_files"),
    path(
        "public_files/", views.public_disk_files, name="public_disk_files"
    ),  # URL для работы с публичной ссылкой
    path(
        "download/<str:file_path>/", views.download_file, name="download_file"
    ),  # URL для загрузки файла
]
