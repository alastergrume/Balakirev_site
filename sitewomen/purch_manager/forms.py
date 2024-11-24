from django import forms

from purch_manager.models import UploadDeficitFiles


class UploadFilesForm(forms.Form):
    file = forms.FileField(label="Файл")


class RunFilesDeficit(forms.Form):
    #  Это виджет, который выводит список всех файлов из базы данных
    file = forms.ModelChoiceField(queryset=UploadDeficitFiles.objects.all(), empty_label='Последний файл',
                                  label='Файлы')
