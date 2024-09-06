import requests
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from typing import Any, Dict, List

CLIENT_ID = "f6352a33c61f4a9eab4f4049ca66d098"
CLIENT_SECRET = "29248fb59bfd4256b6813b134db192e8"
REDIRECT_URI = "https://software-developers.ru"


def home(request):
    return render(request, "home.html", {})


def login(request):
    return redirect(
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )


def oauth_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("login")  # Обработка отсутствия кода

    # Обработка получения токена
    # ... (ваш код)


def user_info(request):
    access_token = request.session.get("access_token")
    if access_token:
        headers = {"Authorization": f"OAuth {access_token}"}
        response = requests.get("https://login.yandex.ru/info", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return render(request, "user_info.html", {"user": user_data})

    return redirect("login")


@api_view(["GET"])
def disk_files(request):
    access_token = request.session.get("access_token")
    if access_token:
        headers = {"Authorization": f"OAuth {access_token}"}

        # Получение файлов
        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources", headers=headers
        )
        if response.status_code == 200:
            files = response.json().get("_embedded", {}).get("items", [])
            return render(request, "disk_files.html", {"files": files})

    return redirect("login")


@api_view(["POST"])
def download_file(request, file_path: str) -> JsonResponse:
    access_token = request.session.get("access_token")
    if access_token:
        headers = {"Authorization": f"OAuth {access_token}"}
        download_url = (
            f"https://cloud-api.yandex.net/v1/disk/resources/download?path={file_path}"
        )

        response = requests.get(download_url, headers=headers)
        if response.status_code == 200:
            download_link = response.json().get("href")
            # Здесь вы можете добавить логику для загрузки файла, если это необходимо
            return JsonResponse({"download_link": download_link})

    return JsonResponse({"error": "Ошибка загрузки файла"}, status=400)


def public_disk_files(request):
    public_link = request.GET.get("public_key")
    if public_link:
        # Логика для работы с публичной ссылкой
        headers = {"Authorization": f'OAuth {request.session.get("access_token")}'}
        response = requests.get(
            f"https://cloud-api.yandex.net/v1/disk/resources?public_key={public_link}",
            headers=headers,
        )
        if response.status_code == 200:
            files = response.json().get("_embedded", {}).get("items", [])
            return render(request, "disk_files.html", {"files": files})
    return render(request, "disk_files.html", {"files": []})
