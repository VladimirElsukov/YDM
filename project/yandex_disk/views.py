import requests
from django.shortcuts import redirect, render

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

    token_response = requests.post(
        "https://oauth.yandex.ru/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
        },
    )

    if token_response.status_code != 200:
        return redirect("login")  # Обработка ошибки получения токена

    token_json = token_response.json()
    request.session["access_token"] = token_json.get("access_token")
    return redirect("user_info")

def user_info(request):
    access_token = request.session.get("access_token")
    if access_token:
        headers = {
            "Authorization": f"OAuth {access_token}",
        }
        response = requests.get("https://login.yandex.ru/info", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return render(request, "user_info.html", {"user_data": user_data})
    
    return redirect("login")  # Перенаправление, если нет токена или ошибка

def disk_files(request):
    access_token = request.session.get("access_token")
    if access_token:
        headers = {
            "Authorization": f"OAuth {access_token}",
        }
        response = requests.get("https://cloud-api.yandex.net/v1/disk/resources", headers=headers)
        if response.status_code == 200:
            files = response.json().get("_embedded", {}).get("items", [])
            return render(request, "disk_files.html", {"files": files})
        else:
            return render(request, "error.html", {})  # Обработка ошибки
    return redirect("login")  # Перенаправление, если нет токена