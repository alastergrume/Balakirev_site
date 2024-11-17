from django.urls import path
from . import views


urlpatterns = [
    path('deficit/', views.index, name='deficit'),
    path('deficit/upload_deficit/', views.about, name='upload_deficit'),
    path('deficit/deficit/button/', views.run_deficit, name='run_deficit'),
]
