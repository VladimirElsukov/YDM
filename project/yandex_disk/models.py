from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название файла")
    size = models.IntegerField(verbose_name="Размер (байты)")  # Размер в байтах
    modified_date = models.DateTimeField(verbose_name="Дата изменения")
    path = models.CharField(max_length=255, verbose_name="Путь")
    mime_type = models.CharField(
        max_length=100, verbose_name="Тип файла"
    )  # Тип файла (например, image/jpeg)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class UserProfile(models.Model):
    yandex_user_id = models.CharField(
        max_length=255, verbose_name="ID пользователя Яндекс"
    )
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(verbose_name="Электронная почта")
    registration_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
