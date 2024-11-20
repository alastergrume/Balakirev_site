from django.db import models
from django.urls import reverse


# Create your models here.

class PublishedManager(models.Manager):
    """
    Класс для кастомного менеджера чтения строк базы данных
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        """
        Класс для автоматического задания статуса. Используется в свойстве is_published
        """
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    # поле для создания слага, он уникальный и индексируемый
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    # В свойстве применяется класс для задания статуса.
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    # Связь с классом Category через связь один ко многим. Используется ForeignKey
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    # Связь с классом TagPost через ManyToMany Многие ко многим
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='women')


    # Определение менеджеров чтения строк базы данных. Если задать кастомный менеджер,
    # то так же необходимо указать менеджер по умолчанию, чтобы он продолжал работать.
    objects = models.Manager()
    published = PublishedManager()

    # При обращении к классу Women, будет возвращаться title строки
    def __str__(self):
        return self.title


    class Meta:
        """
        Класс для сортировки строк в базе данных
        """
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


    def get_absolute_url(self):
        """
        Метод для формирования url адреса с уникальным слагом для каждой записи
        """
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    """
    Класс для добавления категорий, ПЕРВИЧНЫЙ класс для главной таблицы, использует связь один ко многим
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        """
        Автоматическое создание url адреса с уникальным слагом
        """
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    """
    Создание класса для демонстрации связи Многие для многих
    """
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        """
        Метод для формирования url адреса с уникальным слагом для каждой записи
        """
        return reverse('tag', kwargs={'tag_slug': self.slug})

class Husband(models.Model):
    """
    Таблица для отображения мужей. Используется связь один к одному
    """

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name

