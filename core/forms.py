# forms.py
from django import forms

class TextFileForm(forms.Form):
    file = forms.FileField(label="Suba un archivo .txt",
                           widget=forms.ClearableFileInput(attrs={'accept':'.txt'}))
