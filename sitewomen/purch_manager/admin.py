from django.contrib import admin
from .models import UploadDeficitFiles


# Register your models here.

@admin.register(UploadDeficitFiles)
class DeficitAdmin(admin.ModelAdmin):
    # Для отображения информации в админ-панели
    list_display = ('time_create',)
    # Сортировка
    ordering = ['time_create']
    # Пагинация списка
    list_per_page = 5



