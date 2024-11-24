from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.views import View

from .forms import AddPostForm, UploadFileForm, CommentForm
from .models import Women, Category, TagPost, UploadFiles, CommentModel

# Коллекция для вывода меню
menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Дефицит', 'url_name': 'run_deficit'},  # Переход к приложению purch_manager
    {'title': 'Войти', 'url_name': 'login'},
]


def index(request):
    posts = Women.published.all()
    comments = CommentModel.objects.all()
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': posts,
            'comments': comments,
            }
    return render(request, "women/index.html", context=data)


# def handle_uploaded_file(f):
#     # Функция для загрузки файла с оф. док. https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/
#     with open(f"women/media/women/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    """
    Добавление изображений
    """
    # При отправке файла в форме, в Request создается атрибут FILE
    # И к нему потом можно обратиться для сохранения файла
    # Можно использовать функции, которые определены документацией
    # https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/
    if request.method == 'POST':
        forms = UploadFileForm(request.POST, request.FILES)
        if forms.is_valid():
            # handle_uploaded_file(forms.cleaned_data['file'])
            fp = UploadFiles(file=forms.cleaned_data['file'])
            fp.save()
        return redirect('home')
    else:
        forms = UploadFileForm()
    return render(request, "women/about.html", {'title': "О сайте", 'menu': menu, 'form': forms})


def show_post(request, post_slug):  # Получаем из Get запроса id поста
    """
    Отображение статьи
    """
    comment = CommentForm()
    if request.method == "POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            text_of_comment = comment.cleaned_data['comment']
            user = request.user
            post = Women.objects.filter(slug=post_slug)[0]
            CommentModel.objects.create(comment=text_of_comment,
                                        user=user,
                                        post=post,
                                        )
        return redirect('post', post_slug)
    # Обращаемся к базе данных Women, и возвращаем из неё строку, соответствующую slug записи
    post = get_object_or_404(Women, slug=post_slug)
    first_model = Women.objects.get(slug=post_slug)
    comment_text = first_model.comments.all()

    # Формируем словарь из переменных, для их открытия в форме HTML
    data = {
        'title': post.title,
        # Обращаемся к коллекции post (строка из базы данных и сохраняем в ней наименование строки)
        'menu': menu,  # Это меню из глобального уровня, чтобы отрабатывал base.html
        'post': post,  # Это весь объект post
        'comment': comment,
        'comment_text': comment_text,
        'cat_selected': 1,
    }
    return render(request, "women/post.html", data)


class AddPage(View):
    """
    Класс для добавления постов
    """
    def get(self, request):
        form = AddPostForm()
        return render(request, "women/addpage.html", {'menu': menu, 'title': "Добавление статьи", 'form': form})

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, "women/addpage.html", {'menu': menu, 'title': "Добавление статьи", 'form': form})

# Функция для добавления постов, закрыта пока есть класс выше

# def addpage(request):
#     #  В форме, есть метод POST, в случае отправки информации с формы,
#     #  то будут выполнен данный алгоритм
#     if request.method == 'POST':
#         #  Создается объект класса формы, и в него заполняется информация из
#         #  полученной коллекции POST
#         form = AddPostForm(request.POST, request.FILES)
#         # Производится проверка заполненной формы
#         if form.is_valid():
#             # # print(form.cleaned_data)
#             # # Распаковка полученных данных из формы в базу данных
#             # try:
#             #     Women.objects.create(
#             #         **form.cleaned_data)  # Если бы названия полей и названия модели не совпадали, то было бы не возможно распаковать данные подобным образом
#             #     # Возврат на домашнюю страницу
#             #     return redirect('home')
#             # except:
#             #     # Отработка ошибок, связанных с ошибками доабвления в базу данных
#             #     form.add_error(None, "Ошибка добавления поста")
#
#             #  Сохранение в базу дынных в случае связанной с моделью формы
#             form.save()
#             return redirect('home')
#     #  Если запрос GET, то просто создаем объёкт класса формы.
#     else:
#         form = AddPostForm()
#     data = {
#         'title': "Добавление статьи",
#         'menu': menu,  # Это меню из глобального уровня, чтобы отрабатывал base.html
#         'form': form,  # Подключили созданный объект класса
#     }
#     return render(request, "women/addpage.html", data)


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


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)

    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)
