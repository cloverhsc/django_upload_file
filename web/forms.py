from django import forms


class FilesForm(forms.Form):
    fw = forms.FileField()
