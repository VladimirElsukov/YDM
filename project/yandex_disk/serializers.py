from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    name = serializers.CharField()
    size = serializers.IntegerField()
    modified_date = serializers.DateTimeField()
    path = serializers.CharField()
