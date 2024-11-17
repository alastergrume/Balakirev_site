from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect
from women.modules.my_func import input_deficit
from .forms import UploadFilesForm

from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import UploadDeficitFiles

menu = [
    {'title': 'Формирование дефицита', 'url_name': 'upload_deficit'},
    {'title': 'Отображение дефицита', 'url_name': 'run_deficit'},

]




def index(request):
    data = {'title': 'Главная страница',
            'menu': menu,
            }
    return render(request, "purch_manager/index.html", context=data)


# def handle_uploaded_file(f):
#     # Функция для загрузки файла с оф. док. https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/
#     with open("women/media/women/daily_deficit.xlsx", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    # При отправке файла в форме, в Request создается атрибут FILE
    # И к нему потом можно обратиться для сохранения файла
    # Можно использовать функции, которые определены документацией
    # https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/
    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadDeficitFiles(file=form.cleaned_data['file'])
            fp.save()
            # handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFilesForm()
    return render(request, "purch_manager/upload_deficit.html",
                  {'title': "Загрузить файл", 'menu': menu, 'form': form})


def run_deficit(request):
    """
    Функция для просмотра файла дефицита. Берет сохраненный файл и выводит его страницу
    """
    if request.method == 'GET':
        try:
            context = input_deficit(deficit_file='media/uploads_deficit_files/deficit.xlsx')
        except FileNotFoundError:
            return HttpResponse("Файл не найден")

        # Отправляем в форму context, тут DataFrame из функции create deficit
        # и menu для того чтобы пользоваться base.html
        return render(request, 'purch_manager/run_deficit.html', {'context': context,
                                                                  'menu': menu})


def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена"
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
