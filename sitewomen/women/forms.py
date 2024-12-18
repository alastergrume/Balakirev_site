from django import forms
from .models import Category, Husband, Women, CommentModel


class AddPostForm(forms.ModelForm):
    """
    Форма для создания поста
    """
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label='Муж')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

# Для не связанной с моделью формы ввода поста
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea, required=False, label='Контент')
#     is_published = forms.BooleanField(required=False, initial=True, label='Статус')
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категории')
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label='Муж')


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')



class CommentForm(forms.ModelForm):
    """
    Форма для отображения комментариев поста
    """
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": 'form-control',
                "placeholder": "Введите текст комментария",
                "rows": 5
            }
        ),
    )
    class Meta:
        model = CommentModel
        fields = ("comment",)
