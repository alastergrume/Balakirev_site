from django.apps import AppConfig


class PurchManagerConfig(AppConfig):
    # Отображение наименования приложения в админ-панели
    verbose_name = "Загрузка файла дефицита"
    # Системные переменные
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purch_manager'

