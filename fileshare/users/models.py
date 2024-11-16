from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type_choices=(('OP','Operation user'),('CL','Client user'))
    user_type=models.CharField(max_length=2,choices=user_type_choices)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
