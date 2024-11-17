from django import forms


class UploadFilesForm(forms.Form):
    file = forms.FileField(label="Файл")