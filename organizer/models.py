from django.db import models
import os
from datetime import datetime

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    organized_path = models.CharField(max_length=255)

    def __str__(self):
        return self.original_name