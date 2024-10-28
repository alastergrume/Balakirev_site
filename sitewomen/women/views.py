from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
def index(request):
    return HttpResponse("<h1>Главная страница сайта</h1>")


def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>ID: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>Cat_SLUG: {cat_slug}</p>")


def archive(request, year):
    if year > 2023:
        return redirect(index)

    return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")


def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена"
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
