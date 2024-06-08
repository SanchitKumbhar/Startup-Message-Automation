from django import forms
from .models import *  # Import your model

class MyModelForm(forms.Form):  # Use ModelForm instead of Form
    class Meta:
        files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

