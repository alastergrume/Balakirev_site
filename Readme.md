----------------------------------------------------------------------------------------
Порядок действий:
----------------------------------------------------------------------------------------
Устанавливаем пакет django

    -> pip install django

Обновляем pip

    -> python.exe -m pip install --upgrade pip

Смотрим версии 

    -> pip list

>>>
Package  Version
-------- -------
asgiref  3.8.1
Django   5.1.2
pip      24.2
sqlparse 0.5.1
tzdata   2024.2

Ознакомиться с командами Django
    
    -> django-admin
    >>>
    > Available subcommands:
    ...

Для создания проекта команда: 

    -> django-admin startproject sitewomen

Команда создаст проект под названием sitewomen. Как правило, наименование проекта соответствует доменному имени сайта.
Создается пакет конфигурации в папке sitewomen

Заходим в папку проекта

    -> cd sitewomen

Запускаем локальный сервер
    
    -> python manage.py runserver

Запуститься локальный тестовый сервер, который будет доступен по адресу 
http://127.0.0.1:8000/

Чтобы остановить сервер 

    CTR+C или CTRL+BREAK

При первом запуске сервера создается файл базы данных 

    db.sqlite3

Если необходимо изменить порт, то можно запустить его на другом порту: 

    -> python manage.py runserver 4000

------------------------------------------------------------------------------------------------------------------------
Принцип работы фреймворка:
----------------------------------------------------------------------------------------

Модель MTV: Models - Модели
            Templates - Шаблоны
            Views - Представления

                         | --->>> Представление1 (View1) | --->>> Модель (Model)
    Маршрутизация по url |                               |
                         | --->>> Представление2 (View2) | --->>> Шаблоны (Templates)

При запрос от пользователя, например, когда вводит в строке браузера адрес страницы. 
Django проверяет указанные маршруты, и при нахождении совпадения, открывает то или иное представление.
Маршрут соответствует какому либо шаблону
127.0.0.1:8000/
127.0.0.1:8000/category/1/
127.0.0.1:8000/women/madonna/

Представление может быть реализовано в виде функции либо в виде класса, которое отвечает на соответствующий запрос 
Ответом является html страница, которая возвращается обратно пользователю.

Страница отрисовыается по опредленному шаблону. 

Данные в шаблон подставляются так же представлением и берутся из модели, которая взаимодействует с базой данных.
По простому:
Если приходит запрос, то представление, которое связано с этим маршрутом, берет шаблон, подставляет в него данные из
базы и возвращает клиенту в виде html страницы.

------------------------------------------------------------------------------------------------------------------------
Следующим шагом будет создание приложения сайта. 
----------------------------------------------------------------------------------------
Так как в философии Django указано, что нужно для каждой функциональной части сайта, делать отдельное приложение.
Приложения необходимо реализовывать максимально независимыми друг от друга.

Создаем первое приложение, которое будет ядром нашего сайта

Создание нового приложения

    -> python manage.py startapp women

После создается под каталог women с файлами конфигурации и рабочими файлами

Регистрация приложения в файле sitewomen/settings
INSTALD_APPS = [], добавляем имя нашего приложения
Можно прописать просто имя 'women', и при обращении к этому приложению Джанго будет обращаться 
к классу WomenConfig из файла women/apps.py
Поэтому лучше явно указать путь к этому файлу:
    
    'women.apps.WomenConfig'

------------------------------------------------------------------------------------------------------------------------
Следующий шаг - создание обработчика главной страницы и её маршрутизация
----------------------------------------------------------------------------------------
В файле women/views.py пропишем первое представление.

Для этого объявим функцию, на входе, которой будет переменная request
    
    def index(request):

request - ссылка на класс HTTPRequest, которая содержит информацию о запросе (Сессии, куки и т.д.)
на выходе возвращает объект класса HTTPResponse с содержимым ответа
Этот класс нужно импортировать

Потом эту функцию нужно связать с соответстветсвующим адресом.
На глобальном уровне в файле sitewomen/urls.py прописываем путь к созданному файлу.
path('women/', index), Здесь 'women/' это часть адреса в конце, index функция представления в приложении women 
Далее импортируем функцию 
from women.views import index
Для того чтобы Django смог увидеть папку приложения women нужно установить рабочий каталог
Для этого на дириктори проекта sitewomen кликаем правой кнопкой мыши выбираем пункт контекстного меню
Mark Directory As и выбираем Source Root

    path('index/', include('women.urls'))

Пропишем ещё одну функцию представления и маршрут на неё

sitewomen/urls.py

    from women.views import index, categories

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('women/', index),
        path('categories/', categories),
    ]

women/views.py

    ...

    def categories(request):
        return HttpResponse("Вторая страница")

для того чтобы попадать сразу на главную страницу нужно прописать маршрут так:

    path('', index),

Импортировать лучше весь файл vies.py а в маршрутах указывать функции в следующем формате:
views.index и т.д.

будет выглядет так.

    from women import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index),
        path('categories/', views.categories),
    ]

Лучшей практикой будет разделять маршруты приложений, для этого:
Создаем в папке приложения women файл urls.py
Потом, в глобальном файле sitewomen/urls.py подключаем созданный файл через функцию include()
path('', include('women.urls'),
В файле women/urls.py прописываем то же самое, но только уже для каждой функции представления

будет выглядеть так: 
sitewomen/urls.py

    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('women.urls')),
    ]


women/urls.py

    from django.urls import path
    from women import views
    
    
    urlpatterns = [
        path('', views.index),
        path('categories/', views.categories),
    ]

Если в глобальном url прописать  path('women', include('women.urls')), то в адресе всех страниц приложения будет добавляться суффикс women

------------------------------------------------------------------------------------------------------------------------
Настройка запуска сервера через кнопку, а не через команду в терминале. Так же можно будет проводить DEeBAG стандартными средствами PyCharm
----------------------------------------------------------------------------------------
Для этого у кнопки запуска выбираем Edit Configuration
 Добавляем Python конфигурацию через плюсик
 Вводим название проекта
 Выбираем рабочую директорию E:\PycharmProjects\Balakirev_site\sitewomen
 Выбираем наше виртуальное окружение
 В поле Script выбираем файл mange.py проекта
 В поле параметров прописываем runserver
После чего нажимаем кнопку Apply
Теперь можно запускать через зеленый треугольник. И можно так же запустить DeBug выбрав поля для отслеживания процесса работы программы.

------------------------------------------------------------------------------------------------------------------------
Конвертеры значений в маршрутах к функциям представлений.
----------------------------------------------------------------------------------------
У нас есть страничка с категориями. Ссылка на нее имеет следующий вид
http://127.0.0.1:8000/cats/
Предположим, у нас несколько категорий которые необходимо открывать по числовым индексам, для этого ссылка должна выглядеть следующим образом:
http://127.0.0.1:8000/cats/1/
http://127.0.0.1:8000/cats/2/
http://127.0.0.1:8000/cats/3/
и т.д.
Для этого нужно.
Прописаываем в маршруте конвертор и переменная, которя будет содержать целое чслов запросе:
'<int:cat_id>'
Путь теперь будет выглядеть так:

    path('cats/<int:cat_id>/', views.categories),

Эту переменную, 'cat_id' необходимо указать в функции представления

В данном примере она будет принимать то значение, которое будем указывать в ссылке. Сейчас это делается в ручном режиме, для демонстрации наглядности. 
После чего данная переменная должна отображаться на главной странице.
В итоге функция будет иметь следующий вид:

    def categories(request, cat_id):
        return HttpResponse(f"<h1>Вторая страница</h1><p>{cat_id}</p>")

на входе добавили переменную, на выходе выводим её на странице через f строку в теге <p>
Как это работает:
-> при указании в адресе строки какого либо числового значения http://127.0.0.1:8000/cats/1/ 
-> Django находит соответствующий маршрут и сохраняет 1 в переменную cat_id, 
-> После чего передает эту переменную в функцию представления, и уже функция возвращает это значение на главной странице  
Данный конвертер работ только на целые числа. Для других значений должны быть другие конвертеры, например <float:...>
Информация о всех конвертерах в документации в разделе Path converter
https://docs.djangoproject.com/en/5.1/topics/http/urls/#registering-custom-path-converters

Для демонстрации добавим ещё одну функцию представления и маршрут
    
    women/urls.py

    path('cats/<int:cat_id>/', views.categories),
    path('cats/<slug:cat_slug>/', views.categories_by_slug),
    
    womne/views.py

    def categories_by_slug(request, cat_slug):
        return HttpResponse(f"<h1>Статьи по категориям</h1><p>Cat_SLUG: {cat_slug}</p>")

Теперь при вводе в суффиксе адреса числового значения выводится страница с ID
А при вводе текстового значения и даже с указанием цифр и знаков выводится Cat_SLUG

Но если поменять маршруты местами, то при вводе цифрового значения все равно будет отрабатываться SLUG, а второй маршрут не будет отработан никогда
Так как фильтр slug включает в себя более обширный знаков в том числе и цифровой, рассматривая эти значения как строки.

Для чего это нужно:
Можно в маршруте указывать заранее заготовленную функцию, которая к примеру будет возвращать id строки в базе данных, и тогда
будет открываться страница с конкретной записью.

Если конверторов не достаточно, то есть функция re_path(),  которая работает с регулярными выражениями.
Для этого нужно её импортировать
Первый параметр в ней будет регулряным выражением

    re_path(r"^archive/(?P<year>[0-9]{4})/", views.archive),

r"" - строка
archive - префикс
?P<year> - создали перерменную
[0-9] - переменная должна состоять из цифр от 0 до 9
{4} - только четыре цифры в переменной
views.archive - новая функция представления

в функции представления указываем то же самое, что и указывали в других. Так же на входе переменная year, которая передается на выход в HTTPResponse()

    def archive(request, year):
        return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")

при вводе строки http://127.0.0.1:8000/archive/2026/ на странице выводится 

>>>ГОД: 2026

Из минусов неудобная читаемость кода при использовании регулярного выражения
Для более удобной читаемости можно создать свой конвертер, пример есть в официальной документации
Создаем в папке women файл converters.py
В нем класс конвертера (В данном примере взял с оф. док.)

    class FourDigitYearConverter:
        regex = "[0-9]{4}"
    
        def to_python(self, value):
            return int(value)
    
        def to_url(self, value):
            return "%04d" % value

regex = "[0-9]{4}" - Параметры значения регулярного выражения, из цифр от 0 до 9 с длинной в 4 цифры
to_python - преобрзаование фрагмента url  втребуемый тип данных, выдает целые значения
to_url - наоборот преобразовывает данные в требуемый url, целые значения преобразовываются в строку.

women/urls.py
    
    from django.urls import path, re_path, register_converter # импортируем модуль register_converter
    from . import views
    from . import converters # Импортируем все из файла converters.py
    
    # Регистрируем конвертер
    
    register_converter(converters.FourDigitYearConverter, 'year4') # Регистрируем конвертер, где: модуль(наш_конвертер, название конвертера)

    urlpatterns = [
        path('', views.index),
        path('cats/<int:cat_id>/', views.categories),
        path('cats/<slug:cat_slug>/', views.categories_by_slug),
        path('archive/<year4:year>/', views.archive),, # Теперь можно записать конвертер уже в привычной форме, указав его название и добавив переменную
    ]

В данном примере при GET запросе, в конструкцию маршрута попадает строковое значение, после чего , это строковое значение попадает в класс конвертера
и преобразуется с помощью метода to_pyton в числовое значение. Метод срабатывает так как, используются входящие данные, которые исходя из GET запроса
всегда представляют строковое значение. После этого преобразования уже числовое значение отправляется в функцию представления и на выходе мы получаем это значение.


Ключевые моменты:
1. В маршруте можно указывать конвертеры, которые конвертируют те или иные значения из GET запроса 
    в некоторые значения и сохраняют их в каки-либо переменные Значение зависит от того какой конвертер выбран.
        Синтаксис: /<название конвертера:переменная>/
    Эти значения может отправлять в функции представления, 
2. Так же есть встроенная функция re_path() вместо path(), которая может работать с регулярными выражениями в качестве кастомного конвертера.
    Из минусов, сложная читабельность кода. 
   Синтаксис: re_path(r"^archive/(?P<year>[0-9]{4})/", views.archive),
3. Еще есть вариант создания своего конвертера. Для этого добавляется файл converters.py и в нем прописывается класс с заданными методами преобразования значений. 
    В этом случае импортируется встроенный модуль register_converter, Регистрируется созданный класс и назначается его имя
   А в маршруте в этом случае указывается конвертер уже с понятным синтаксисом: /<название конвертера:переменная>/
    

------------------------------------------------------------------------------------------------------------------------
Дополнительные параметры в GET-Запросах
----------------------------------------------------------------------------------------
В функции представления есть параметр request, который через метод .GET можно вывести эти параметры
Для примера в функции представления добавил следующее

    print(request.GET)

в строке браузера ввел дополнительные параметры: 

    http://127.0.0.1:8000/cats/slag/?name=Gagarina&type=Pop

в итоге в консоли у меня распечатались дополнительные параметры из переменной request
    
    <QueryDict: {'name': ['Gagarina'], 'type': ['Pop']}>

что соответствует вот этому запросу: ?name=Gagarina&type=Pop


----------------------------------------------------------------------------------------
Обработка исключений
----------------------------------------------------------------------------------------
При вводе несуществующего URL В режиме DEBUG=True отображается страница Django с зарегистрированными путями
Но можно переключить в DEBUG=False, то необходимо в ALLOWED_HOSTS = [] ввести доменную страничку и тогда будет выводится 
сообщение Page Not Found
    
    DEBUG=False
    ALLOWED_HOSTS = ['127.0.0.1']

Для того чтобы выводилась нужная нам страница необходимо сделать следующее:
в глобальном URLS нужно прописать специальный обработчик 

    from women.views import page_not_found    

    Переменная зарезервированная в Django. Если неправильно написать, работать не будет
    handler404 = page_not_found

Мы определили переменную в которую направляем функцию представления для обработки исключения 404
и эту функцию определим в файле views приложения women

    from django.http import HttpResponseNotFound

    def page_not_found(request, exception):
    """
    Функция представление для обработки исключения PageNotFoundError
    :return: Страницу с надписью "Страница не найдена" 
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

Здесь можно сделать переход на Главную страницу.
Так же можно в любом месте программы в функциях-представлениях сгенерировать ошибку 404 и тогда мы попадем на обрботку этого исключения через указанный обработчик
Пример: 

    def archive(request, year):
        if year > 2023:
            raise Http404()
        
        return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")

Теперь, если отправть GET-запрос в данную функицю представления с несоответствующим значением переменно year, то будет сгенерировано исключение 404 и автоматически
будет запущена её обработка, и нас снова перекинут на страницу "Страница не найдена"

    http://127.0.0.1:8000/archive/2024/
    Страница не найдена

    http://127.0.0.1:8000/archive/2023/
    Архив по годам
    ГОД: 2023

https://docs.djangoproject.com/en/5.1/ref/urls/
Здесь собраны обработчики подобных исключений. 400, 403, 404, 500


------------------------------------------------------------------------------------------------------------------------
Перенаправление (redirect)
----------------------------------------------------------------------------------------
код 301 - страница перемещена на другой постоянный url
код 302 - страница перемещена временно на другой url
для примера:

    def archive(request, year):
        if year > 2023:
            return redirect('/') # Адрес главной страницы, можно указать какой-то другой
    
        return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")

return redirect('/') -  в этом случае будет перемещено с кодом 302 
чтобы перемещение было с кодом 301, то необходимо указать параметр permanent=True

    def archive(request, year):
        if year > 2023:
            return redirect('/', permanent=True) # Адрес главной страницы, можно указать какой-то другой
    
        return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")

>>> [25/Oct/2024 22:21:07] "GET /archive/2026/ HTTP/1.1" 301 0

Так же можно в redirect отправлять сразу функцию представления на страницу, которой необходимо перейти.

    def archive(request, year):
        if year > 2023:
            return redirect(index) # Указана функция представления Главной страницы сайта
    
        return HttpResponse(f"<h1>Архив по годам</h1><p>ГОД: {year}</p>")



******************************************************************************************
Эксперимент: 
В качестве эксперимента, создал шаблон main страницы под названием main.html и подключил на функцию представления 
index
Теперь отображается надпись Главная страница и кнопка со ссылкой на шаблон run_deficit.html по имени run_deficit в маршрутизации.
В urls добавил маршрут на страницу path('deficit/button/', views.run_deficit, name='run_deficit'), run_deficit,
который ссылается на функцию run_deficit во views.py.
При нажатии на ссылку в функцию поступает коллекция request. При условии, что в request метод GET, 
то срабатывает функция numb_calc() в модуле my_func, который расположен в папке modules.
Выполняется некий алгоритм и возвращается значение вычислений в виде списка.
Далее через render это значение через переменную context отправляется в шаблон run_deficit.html
В шаблоне данный список перебирается циклом for и выводится на странице сайта.

******************************************************************************************
----------------------------------------------------------------------------------------
Шаблоны
----------------------------------------------------------------------------------------
Для начала нам необходимо импортировать модуль, который будет загружать шаблоны:
    
    from django.template.loader import render_to_string

Далее воспользуемся функцией index модуля views.py

    def index(request):
        t = render_to_string("Путь к шаблону index.html")
        return HttpResponse(t)
Здесь в функцию render_to_string занесем путь к шаблону, потом передадим переменную t в HttpResponse
Лучше шаблон нужно размещать в каталоге приложения templates/women/
Модуль render_to_string нужно для того, чтобы загрузить переменную в статическую переменную
и потом вызывать из разных мест в коде.
Для простого вызова шаблона можно использовать модуль render, который импортируется из
    
    from django.shortcuts import render

Здесь нужно первым параметром отправить переменную request, а вторым, путь к шаблону

------------------------------------------------------------------------------------------

Конструкции в шаблонах

Запишем {{title}} в шаблоне
Чтобы передать указанный параметр в шаблон, то в функции представления нужно создать словарь и передать его в шаблон
Выглядеть будет следубшим образом:
    
    def index(request):

    data = {'title': 'Главная страница'}
    return render(request, "women/index.html", data)

либо можно сразу передать словарь:

    def about(request):
    return render(request, "women/about.html", {'title': "О сайте"})

При передаче ключ в словаре title будет доступен в шаблоне, 
и его значение может быть вызвано с помощью переменной {{title}}

Тем самым мы можем в шаблон передавать переменные и отображать их в шаблоне.

Пропишем меню сайта и отправим в шаблон
    
    menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

    def index(request):
  
    data = {'title': 'Главная страница',
            'menu': menu,
            }
    return render(request, "women/index.html", data)

в шаблон укажем 
    
    <p>{{menu}}</p>

Выйдет строковое представление словаря

    ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

Как вывесьт одно из значений
Если просто указать 
    
    <p>{{menu[0]}}</p>
То будет ошибка синтаксеррор
Дело в том, что Django не поддерживает такое обращение.

Что бы вывести атрибут ключа, нужно следовать следующему синтаксису:

    <p>{{menu.0}}</p>

Так можно отображать данные в шаблонах

----------------------------------------------------------------------------------------
Фильтры для шаблонов:
----------------------------------------------------------------------------------------
https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#add

Фильтры нужны для того чтобы в шаблоне выполнять какие либо манипуляции с данными. 
К примеру возьмем фильтр add, который добавляет к значению указанный аттрибут
в словарь data добавим значение: 'float': 2.5,
а в шаблоне укажем фильтр в следующем синтаксисе:

    <p>{{ float|add:"2" }}</p>

Где add это название фильтра и пишется он после "|" вертикального слэша, 
после наименования фильтра через двоеточие ":" указываем значение, которое будет добавляться

Можно применять несколько фильтров подряд

    <p>{{ menu|first|lower }}</p>

Выделяется первый элемент из списка и в нижнем регистре.

Ещё один пример:

    <p>{{ menu|join:" | " }}</p>

Вывод будет таким:

    О сайте | Добавить статью | Обратная связь | Войти

Перевод строк в слаги:

    <p>{{ "The Main Page"|slugify }}</p>

Результат:

    the-main-page

Фильтры можно так же импортировать в Python и использовать как функции. Для этого нужно 
импортировать модуль

    from django.template.defaultfilters import slugify
    
Добавим в словарь data ещё одно значение
  
    'url': slugify("The main page")
и выведем в шаблон
    
    <p>{{ url }}</p>

Результат:

    the-main-page


-------------------------------------------------------------------------------------------
Тэги в шаблонах
-------------------------------------------------------------------------------------------
Тэги прописываются в шаблонах
Синатксис

{% название тэга [параметр] %}

-------------------------------------------------------------------------------------------
Формирование главной страницы
-------------------------------------------------------------------------------------------
Создадим ещё одну коллекцию в которой будет содержаться информация о постах
    
    data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'id_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'id_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'id_published': True},
    ]
и добавим в фцункцию index:
        
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': data_db,
            } 

Теперь через переменную posts мы отправляем в шаблон ещё и коллекцию data_db 

В шаблоне делаем разметку для цикла for, который будет перебирать словари из переменной post
и выводить информацию о наименовании статьи и её содержимом.

    <ul>
         {% for p in posts %}
         <li>
             <h2>{{ p.title }}</h2>
             <p>{{p.content}}</p>
             <hr>
         </li>
         {% endfor %}
     </ul>

Для того чтобы отделить некоторые статьи по параметру, то можно использовать тэг if

В коде есть черта <hr>, которая отображается в конце вывода на странице, чтобы её убрать нужно сделать:

    добавим перед <hr> тэг {% if not forloop.last %}

>>> Объяснение
    Если не последний цикл, то тэг hr записываем, а если последняя, то hr не выводится

forloop.last является переменной цикла, так же есть и другие, о них более подробно написано в документации
https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#for

Ещё нужно выводить только те статьи, которые были опубликованы т.е. id_published=True
ДЛля этого блок for будет следующим:

     <ul>
         {% for p in posts %}
         {% if p.id_published == True %}
         <li>
             <h2>{{ p.title }}</h2>
             <p>{{p.content}}</p>
             {% if not forloop.last %}
             <hr>
             {% endif %}
         </li>
         {% endif %}
         {% endfor %}
     </ul>

---------------------------------------------------------------------------------------------------------
Шаблонный тэг в шаблоне
---------------------------------------------------------------------------------------------------------

Ссылки в шаблонах можно указывать следующим синтаксимом

    <a href="адрес страницы">Текст ссылки</a>

Укажем в шаблоне следующую ссылку: 
   
     <p>{{p.content}}</p>
             <p><a href="post/p.{{id}}">Читать пост</a></p>

Теперь под каждым постом будет ссылка
Здесь мы ссылаемся на конкретный пост по его id

Но в этом случае адресс захардкожен в шаблоне, поэтому при изменениях нужно будет все переделывать.

Динамическое формирование вэб-адресов необходимо использовать тэг URL.
----------------------------------------------------------------------

При нажатии на ссылку на пост, совершается переход на страницу, где в адресе будет содержаться
индекс поста. Это происходит потому что в шаблоне в ссылке формируется адрес страницы с id поста

    http://127.0.0.1:8000/post/1
    или
    http://127.0.0.1:8000/post/3

Для того чтобы формирование url происходило динамически, и django знал к какой функции представления,
а следовательно к шаблону обращаться, нужно в шаблоне index.html преобразовать ссылки в соответствии со 
следующим синтаксисом:

    Синтаксис:
    {% url 'some-url-name' arg1=v1 arg2=v2 %}

Теперь строка с формированием строки примет следуюший вид:

    <p><a href="{% url 'post' p.id %}">Читать пост</a></p>
Здеси мы заддействуем тэг url в который прередаем имя маршрута post/ и целочисленное значение id поста.

Далее в urls прописываем путь, который будет отправлять в шаблон целочисленное число через переменную post_id

    path('post/<int:post_id>', views.show_post, name='post'),

Объявляем функцию представления show_post() в файле views.py

    def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи {post_id}')

Смысл такой:

В маршрутах прописан путь, и фильтр <int>:post_id будет сохранять эту перемеменную, в post_id
после чего значение будет передано в функцию представления show_post() и возвращено через 
HttpResponse на страницу сайта

-------------
Добавление ссылок для Главного меню
-------------
Добавим маршруты: 

    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

Отображение меню нужно сформировать в виде списка словарей.
У каждого наименования страницы теперь есть наименование маршрута
    
    menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]

После этого объявим указанные функции в файле views.py

В шаблоне index.html пропишем следующий блог для отображения menu

    <ul>
        <li><a href="{% url 'home' %}">Главная страница</a></li>
        {% for item in menu %}
        # Если не последний, то отображается простой li, если последний, то отображается 
        # li с темой офорлмения класса last
        {% if not forloop.last %}<li>{% else %} <li  class="last">{% endif %}
            <a href="{% url item.url_name %}">{{item.title}}</a>
        </li>
        {% endfor %}
    </ul>

Теперь у нас отображается главное меню и мы можем кликать на ссылки этого меню

---------------------------------------------------------------------------------------------
Шаблон base.html
---------------------------------------------------------------------------------------------
Для устранения недостатка Dry Repeat Yourself создается базовый шаблон
Создаем каталог на уровне приложения в папке sitewomen
В нем создаем файл base.html
Для работы с этим файлом необходимо в настройках указать к нему путь
    
    Раздел TEMPLATES в файле settings.py

            'DIRS': [
            BASE_DIR / 'templates',
        ],

В файле base.html делаем разметку, которая будет отображаться на всех страницах
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{title}}</title>
    </head>
    <body>
    <ul>
        <li><a href="{% url 'home' %}">Главная страница</a></li>
        {% for item in menu %}
    
        {% if not forloop.last %}<li>{% else %} <li  class="last">{% endif %}
    
            <a href="{% url item.url_name %}">{{item.title}}</a>
        </li>
        {% endfor %}
    </ul>
    
    {% block content %}
    
    {% endblock %}
    </body>
    </html>

Здесь указывается Главное меню с ссылками 
и блок с указанием тэга block
    
    {% block content %}
    
    {% endblock %}

В этом блоке и будет выводится информация со странице, которую будем подключать к базовому шаблону
Какбы расширяя его. 
content в данном случае означает имя блока для расширения. тем самым этих блоков может быть много разных.

Для подлкючения к шаблону страницы в шаблоне с ней нужно указать 

    {% extends 'base.html' %}

далее нужно указать тот же блок и в нем прописать ту разметку, которую нужно добавить в базовый шаблон
 
    {% extends 'base.html' %}

    {% block content %}
    
    <h1>{{ title }}</h1>
         <ul>
             {% for p in posts %}
             {% if p.id_published == True %}
             <li>
                 <h2>{{ p.title }}</h2>
                 <p>{{p.content}}</p>
                 <p><a href="{% url 'post' p.id %}">Читать пост</a></p>
                 {% if not forloop.last %}
                 <hr>
                 {% endif %}
             </li>
             {% endif %}
             {% endfor %}
         </ul>
    {% endblock %}

Можно так же включать один шаблон в другой
Например на главной странице хотим отображать ссылки на рубрики

    <nav>
        <a href="#">Актрисы</a>
        <a href="#">Певицы</a>
        <a href="#">Спортсменки</a>
    </nav>

и эту информацию мы хотим отображать только на Главной странице.
Для этого мы можем воспользоваться тэгом include

    {% include 'women/includes/nav.html'%}

А в файл nav.html поместим ссылки
так же в файле nav.html так же доступны все переменные из подключаемого файла.
Но можно закрыть эту вожможность, либо добавить какие-то переменные
    
    {% include 'women/includes/nav.html' only%} - закрываем доступ к переменным
    {% include 'women/includes/nav.html' only with title2='dfbdkmlk'%} - закрыли доступ к переменным и отправили туда свою переменную, её так же нужно вызывать в шаблоне для отображения


---------------------------------------------------------------------------------------------
Подключение статических файлов
---------------------------------------------------------------------------------------------

Для подключения статических файлов в режиме Debug нужно папку stativ создавать в папке приложения 
а в ней ещё одну папку с наименование приложения.
После того как проект будет размещен на хосте, все статиеческие файлы необходимо собрать в одну папку 
static в корне проект, для этого есть команда 
    
    python manage.py collectstatic

После чего из этой папки файлы будет подтягивать nginx
Сейчас будем работать в режиме Debuge

Чтобы подключить статический файл необходимо в шаблоне указать тэг 
    
```html
    {% load static %}
```

сделали это для base.html

делее в блоке <head> подключаем файл

    <link type="text/css" href="{% static 'women/css/style.css' %}" rel="stylesheet" />

Так же автор рассказывает про создание тегов, оставил эту тему на потом.

Потом скачал с Github файлы статики и сайт стал неузнаваемым.

---------------------------------------------------------------------------------------------
Тэги
---------------------------------------------------------------------------------------------
Пропустил пока этот блок


---------------------------------------------------------------------------------------------
База данных
---------------------------------------------------------------------------------------------
В Django есть встроенная система ORM, которая взаимодействует с базой данных через классы Python.
Ссылка на официальную документацию:
https://docs.djangoproject.com/en/5.1/ref/models/fields/
Приложение для просмотра базы данных - SQLiteStudio

Для создания таблицы базы данных создается класс в файле models.py 

```python
from django.db import models


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
```

Чтобы создать таблицу необходимо в консоли ввести команду:

    python manage.py makemigrations

Причем будет создан commit. Создается файл миграции в папке migrations
Для его применение необходимо выполнить команду 

    python manage.py migrate

При создании, или изменении таблиц, необходимо применять миграции, которые будут вносить изменения в базу данных

Чтобы просмотреть sql запрос, который будет отправлен в базу данных служит следующая команда:

    python manage.py sqlmigrate women 0004

Данная команда не применяет изменения.


---------------------------------------------------------------------------------------------
Работа с таблицами
---------------------------------------------------------------------------------------------
CRUD
Create
Read
Update
Delete

Записи объекта класса модели
Класс описывает структуру таблицы
А отдельный объект класса представляет из себя одну запись таблицы

Для взаимодействия с базой данных в интерактивном режиме:

    python manage.py shell

Для работы нужно импортировать конкретную модель
Импортируем модель в ORM Django
    
    from women.models import Women

Для добавления записи, нужно создать объект класса

    Women(title='Анджелина Джоли', content='Биография Анджелины Джоли')
    
Остальные параметры заполняются автоматически
Созадался новый объект:
    
    <Women: Women object (None)>

Данные в базу не добавились, просто был создан объект класса. 
Для записи нужно выполнить следующее
Нужно присвоить объект к переменной

    w1 = _

Потом применить метод save()

    w1.save()

После запислась строчка
Для просмотра данных нужно указать атрибут(поле)

    w1.title
    w1.id
    w1.content
    и т.д.

Вместо id в Django используют pk от слова prymary key
Так же можно посмотреть sql запрос, который был выполнен, командой
    
    from django.db import connection
    connection.queries

    [{'sql': 'INSERT INTO "women_women" ("title", "content", "time_create", "time_update", "is_published") VALUES (\'Анджелина Джоли\', \'Биография Анджелины Джоли\', \'2024-11-17 18:22:01.028225\', \'2024-11-17 18:22:01.028225\', 1
    ) RETURNING "women_women"."id"', 'time': '0.015'}]

Для улучшения консоли для работы с ORM
    
    File -> Settings -> Project -> Python interpretator -> new -> ipython

И еще один плагин

    django-extensions
        
После установки нужно привязать его к проекту
       
https://github.com/django-extensions/django-extensions?ysclid=m3lxz1k2lv12323526 

    git@github.com:django-extensions/django-extensions.git

Добавим в INSTALLED_APPS строчку 'django_extensions',
Для использования команда:

    python manage.py shell_plus     # простой вид. Импортируются все модули и приложения проекта автоматически
    python manage.py shell_plus --print-sql     # Для автоматического распечатывания запросов


---------------------------------------------------------------------------------------------
Команды для работы с базой в интерактивном режиме
---------------------------------------------------------------------------------------------
Есть стандартный менеджер записей objects, с помощью которого можно выполнять запросы к базе данных
Добавление записи
метод create() модуля objects

    Women.objects.create(title='Ума Турман', content='Биография Ума Турман')
    В этом случае сразу заносится строчка в базу, без использования метода save()

    INSERT INTO "women_women" ("title", "content", "time_create", "time_update", "is_published")
    VALUES ('Ума Турман', 'Биография Ума Турман', '2024-11-17 18:48:41.903817', '2024-11-17 18:48:41.903817', 1) RETURNING "women_women"."id"

Чтение записей
метод all() модуля objects

    Women.objects.all()

Одна запись: 

    Women.objects.all()[0]

Метод filter()

     Women.objects.filter(title="Энн Хэттуэй")

Так же есть люкапы. В документации как Field lookups
    
    Women.objects.filter(pk__gt=2)
    Выбор записей, с индентификатором больше двух
    WHERE "women_women"."id" > 2

Метод exclude() - исключает строку по выбранному аттрибуту

Все эти запросы возвращают список записей, для возврата строки одной записис, нужно использовать метод get()

    Women.objects.get(pk=2)
    '''
    WHERE "women_women"."id" = 2
    '''

order_by()

    Women.objects.all().order_by('title')
         ORDER BY "women_women"."title" ASC
    
    Women.objects.all().order_by('-title')
        ORDER BY "women_women"."title" DESC

Изменение записи

    wu = Women.objects.get(pk=2)
    wu.title = "Марго Робби"
    wu.content = 'Биография Марго Робби'
    wu.save()
    
        UPDATE "women_women"
            SET "title" = 'Марго Робби',
               "content" = 'Биография Марго Робби',
               "time_create" = '2024-11-17 18:29:17.841122',
               "time_update" = '2024-11-17 19:15:19.001221',
               "is_published" = 1
            WHERE "women_women"."id" = 2

Так же есть метод update()

Удаление методом delete()


----------------------------------------------------------------------
Отображение статей по слагам
----------------------------------------------------------------------

Все сделал, но комментарии пропустил. Видео 22
Видео 23 тоже пропустил

-----------------------------------------------------------------------
Создание связей в базе данных
-----------------------------------------------------------------------

