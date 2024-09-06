import requests
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from typing import Any, Dict, List
from .models import File

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
    if not access_token:
        return redirect("login")

    # Получаем файлы с Яндекс.Диска и кэшируем их в базе данных
    files_data = fetch_files_from_yandex_disk(access_token)

    # Обновляем базу данных
    for file_data in files_data:
        File.objects.update_or_create(
            name=file_data["name"],
            defaults={
                "size": file_data.get("size", 0),
                "modified_date": file_data.get("modified", None),
                "path": file_data["path"],
                "mime_type": file_data.get("mime_type", "unknown"),
            },
        )

    # Получаем все файлы из базы данных
    files = File.objects.all()

    # Получаем параметр фильтрации из запроса
    file_type = request.GET.get("file_type", "")

    # Фильтрация файлов по типу
    if file_type:
        files = files.filter(mime_type=file_type)

    return render(request, "disk_files.html", {"files": files})


def clear_cache(request):
    if "files" in request.session:
        del request.session["files"]
    return redirect("disk_files")


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

# Обработка скачивания нескольких файлов:
@api_view(["POST"])
def download_multiple_files(request) -> JsonResponse:
    access_token = request.session.get("access_token")
    if access_token:
        files = request.POST.getlist("files")
        download_links = []

        headers = {"Authorization": f"OAuth {access_token}"}
        for file_path in files:
            download_url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={file_path}"
            response = requests.get(download_url, headers=headers)
            if response.status_code == 200:
                download_link = response.json().get("href")
                download_links.append(download_link)

        return JsonResponse({"download_links": download_links})

    return JsonResponse({"error": "Ошибка загрузки файлов"}, status=400)


def fetch_files_from_yandex_disk(access_token: str) -> List[Dict[str, Any]]:
    """
    Запрашивает список файлов у API Яндекс.Диска.

    Args:
        access_token (str): Токен доступа для API.

    Returns:
        List[Dict[str, Any]]: Список файлов на Яндекс.Диске.
    """
    headers = {"Authorization": f"OAuth {access_token}"}
    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources", headers=headers
    )

    if response.status_code == 200:
        return response.json().get("_embedded", {}).get("items", [])
    else:
        # Обработка ошибок, можно бросить исключение или вернуть пустой список
        return []
