from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    name = serializers.CharField()
    size = serializers.IntegerField()
    modified_date = serializers.DateTimeField()
    path = serializers.CharField()


from rest_framework import serializers
from .models import File, UserProfile


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["name", "size", "modified_date", "path", "mime_type"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["yandex_user_id", "name", "email", "registration_date"]
