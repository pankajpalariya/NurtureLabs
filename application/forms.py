from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User



class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','password', 'name']
    
    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #     del self.fields['password']
