from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect
from women.modules.my_func import calc_numbers
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Сделать дефицит', 'url_name': 'run_deficit'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'id_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'id_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'id_published': True},
]


def index(request):
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': data_db,
            }
    return render(request, "women/index.html", data)


def about(request):
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


def run_deficit(request):
    numb1 = [1, 2, 3]
    if request.method == 'GET':
        context = calc_numbers(numb1)
        return render(request, 'women/run_deficit.html', {'context': context, 'menu': menu})
