from .views import *
from django.urls import path

urlpatterns = [

    # File APIs
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('generate-download-link/<str:file_name>/', GenerateDownloadLinkView.as_view(), name='generate-download-link'),
    path('download/<str:token>/', DownloadFileView.as_view(), name='download-file'),
    path('available-files/', FilesView.as_view(), name='list-available-files'),
]