from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import Women, Category

# Коллекция для вывода меню
menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Дефицит', 'url_name': 'deficit'},  # Переход к приложению purch_manager
    {'title': 'Войти', 'url_name': 'login'},
]

# Временная коллекция статей
data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


def index(request):
    posts = Women.published.all()
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': posts,
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


def show_post(request, post_slug): # Получаем из Get запроса id поста
    # Обращаемся к базе данных Women, и возвращаем из неё строку, соответствующую ID записи
    post = get_object_or_404(Women, slug=post_slug)
    # Формируем словарь из переменных, для их открытия в форме HTML
    data = {
        'title': post.title, # Обращаемся к коллекции post (строка из базы данных и сохраняем в ней наименование строки)
        'menu': menu, # Это меню из глобального уровня, чтобы отрабатывал base.html
        'post': post, # Это весь объект post
        'cat_selected': 1,
    }
    return render(request, "women/post.html", data)


def addpage(request):
    return HttpResponse("Добавление строки")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'women/index.html', context=data)

def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена"
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
