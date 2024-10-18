from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

class CustomAuthorCreationForm(UserCreationForm):
    class Meta:
        model = Author  
        fields = ("username", "password1", "password2") 

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) 
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        
        author = super().save(commit=False)
        author.host = f"http://{self.request.get_host()}/api/"  
        if commit:
            author.save()
        return author