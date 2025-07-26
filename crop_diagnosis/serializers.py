# yourapp/serializers.py
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
import uuid

class ImagePromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    image_base64 = serializers.CharField()

    def validate_image_base64(self, value):
        try:
            format, imgstr = value.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
            return data
        except Exception:
            raise serializers.ValidationError("Invalid base64 image format.")
