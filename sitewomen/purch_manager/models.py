from django.db import models


# Create your models here.
class UploadDeficitFiles(models.Model):
    file = models.FileField(upload_to="uploads_deficit_files/%Y/%m/%d", verbose_name="Название файла")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        # Отображение названия приложения в админ-панели
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.file)
