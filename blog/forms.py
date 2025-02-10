from django import forms
from .models import Blog


class addform(forms.ModelForm):
    class Meta:
        model=Blog
        fields=["title","description","status"]

class editform(forms.ModelForm):
    class Meta:
        model=Blog
        fields=["title","description"]
