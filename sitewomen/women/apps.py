from django.apps import AppConfig


class WomenConfig(AppConfig):
    # Отображение наименования приложения в админ-панели
    verbose_name = "Задачи"
    # Системные переменные
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'


