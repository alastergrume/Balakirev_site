from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect

from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Дефицит', 'url_name': 'deficit'},  # Переход к приложению purch_manager
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


def index(request):
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': data_db,
            }
    return render(request, "women/index.html", context=data)


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

    return render(request, "women/about.html", {'title': "О сайте", 'menu': menu})


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи {post_id}')


def addpage(request):
    return HttpResponse("Добавление строки")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена"
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
