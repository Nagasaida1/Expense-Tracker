from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.
from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(max_length=30,widget=forms.PasswordInput) # widget is used to encrypt the password

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']


class UserForm1(UserCreationForm):
    class Meta:
        model=User
        fields=['username']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    

    def __str__(self):
        return self.user.username
