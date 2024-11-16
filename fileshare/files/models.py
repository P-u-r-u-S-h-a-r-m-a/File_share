from django.db import models
from users.models import User
from .validators import validate_file_type
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)    
    class Meta:
        abstract = True  


class FileUpload(BaseModel):
    file_name = models.CharField(max_length=100, unique=True) 
    file = models.FileField(upload_to='uploads/', validators=[validate_file_type])
    uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="uploaded_files")

    def __str__(self):
        return self.file_name
