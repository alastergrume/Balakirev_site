from django.contrib import admin
from .models import Women, Category


# Register your models here.

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # Для отображения информации в админ-панели
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat')
    # Кликабельность заданного свойства
    list_display_links = ('id', 'title')
    # Сортировка
    ordering = ['time_create', 'title']
    # Для возможности редактирования
    list_editable = ('is_published',)
    # Пагинация списка
    list_per_page = 5


# Без использования декоратора класса
# admin.site.register(Women, WomenAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Для отображения информации в админ-панели
    list_display = ('id', 'name')
    # Кликабельность заданного свойства
    list_display_links = ('id', 'name')
