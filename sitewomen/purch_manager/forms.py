from django import forms

from purch_manager.models import UploadDeficitFiles


class UploadFilesForm(forms.Form):
    file = forms.FileField(label="Файл")


class RunFilesDeficit(forms.Form):
    file = forms.ModelChoiceField(queryset=UploadDeficitFiles.objects.all(), empty_label='Последний файл',
                                  label='Файлы')
