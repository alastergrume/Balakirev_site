from django.db import models


# Create your models here.
class UploadDeficitFiles(models.Model):
    file = models.FileField(upload_to="uploads_deficit_files")
