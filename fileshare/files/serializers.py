from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = FileUpload
        fields = ('id', 'file', 'file_name', 'uploaded_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uploaded_by', 'created_at', 'updated_at') 

