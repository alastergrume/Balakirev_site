"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from women.views import page_not_found
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),  # Направляемся на URLS  в приложении women
    path('', include('purch_manager.urls')),  # Направляемся на URLS в приложении purch_manager
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработка исключения PageNotFoundError. При вводе не существующего URL обрабатывается функция представления
# women.views.page_not_found. #Переменная зарезервированная в Django. Если неправильно написать, работать не будет

# Для отображения не найденной страницы в режиме Debug = False
if not settings.DEBUG:
    handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"


