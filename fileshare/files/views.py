from users.models import *
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from django.core.signing import TimestampSigner, BadSignature
from django.conf import settings
from django.http import FileResponse
import os
from django.core.exceptions import ValidationError
signer = TimestampSigner()


class FilesView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        
        files=FileUpload.objects.all()
        serializer = FileUploadSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.user_type != 'OP':
            return Response({'detail': 'Only Ops Users can upload files.'}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        file_name = file.name

        if FileUpload.objects.filter(file_name=file_name).exists():
            return Response({"detail": "A file with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            serializer = FileUploadSerializer(data={'file': file, 'file_name': file_name})
            if serializer.is_valid():
                serializer.save(uploaded_by=request.user)
                return Response({'detail': 'File uploaded successfully.', 'file': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'detail': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_name):
        if request.user.user_type != 'CL':
            return Response({'detail': 'Only Client Users can access download links.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            file = FileUpload.objects.get(file_name=file_name)
        except FileUpload.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate signed token and download URL
        token = signer.sign(file.file_name)  
        download_url = f"{settings.HOST_URL}/download/{token}"

        return Response({'download_url': download_url}, status=status.HTTP_200_OK)



class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        try:
            file_name = signer.unsign(token, max_age=3600)  # Validate the token
        except BadSignature:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the file by its name
        try:
            file = FileUpload.objects.get(file_name=file_name)
        except FileUpload.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check file existence
        file_path = file.file.path
        if not os.path.exists(file_path):
            return Response({'detail': 'File no longer exists on the server.'}, status=status.HTTP_410_GONE)

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file.file_name)
