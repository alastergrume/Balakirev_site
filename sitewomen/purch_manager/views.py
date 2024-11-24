from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponse, redirect
from .modules.my_func import input_deficit
from .forms import UploadFilesForm, RunFilesDeficit

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



def about(request):
    """
    Функция сохранения файлов дефицита
    """

    # При отправке файла в форме, в Request создается атрибут FILE
    # И к нему потом можно обратиться для сохранения файла
    # Можно использовать функции, которые определены документацией
    # https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/

    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadDeficitFiles(file=form.cleaned_data['file'])
            fp.save()

            return redirect('run_deficit')
    else:
        form = UploadFilesForm()
    return render(request, "purch_manager/upload_deficit.html",
                  {'title': "Загрузить файл", 'menu': menu, 'form': form})


def run_deficit(request):
    """
    Функция для просмотра файла дефицита. Берет сохраненный файл и выводит его страницу
    """
    # Возвращаем путь до последнего созданного файла дефицита, и отправляем в функцию для формирования потребности

    # Форма для выбора файла формирования дефицита
    form = RunFilesDeficit()
    if request.method == 'POST':
        #  Вытаскиваем значение id из request
        id_pk = request.POST['file']
        #  Ищем позицию по id
        file_path_id = UploadDeficitFiles.objects.filter(pk=id_pk)
        #  Возвращает путь к файлу, который был выбран в форме
        context = input_deficit(path_to_file=f'media/{file_path_id[0]}')
        return render(request, 'purch_manager/run_deficit.html', {'context': context,
                                                                  'menu': menu, 'form': form})
    # print(file_path)
    if request.method == 'GET':
        #  Формируем путь к файлу из базы по последнему добавленному элементу
        file_path = f'media/{UploadDeficitFiles.objects.latest('time_create')}'
        try:
            # отправляем в функцию
            context = input_deficit(path_to_file=file_path)
        except FileNotFoundError:
            return HttpResponse("Файл не найден")

        # Отправляем в форму context, тут DataFrame из функции create deficit
        # и menu для того чтобы пользоваться base.html
        return render(request, 'purch_manager/run_deficit.html', {'context': context,
                                                                  'menu': menu, 'form': form})


def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена"
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
