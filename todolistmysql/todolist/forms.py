from django import forms
from .models import Task, UserProfile
from django.forms import ModelForm, TextInput, EmailField, PasswordInput,CharField,CheckboxInput

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed']
        
        widgets = {
                'title': TextInput(attrs={
                    'class': "form-control",
                    'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                    'placeholder': 'Title'
                }),
                'completed': CheckboxInput(attrs={
                    'class': "form-control btn-check",
                    'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                    'placeholder': 'Title'
                }),
        }
        

            
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserCreateForm(UserCreationForm):
    
    password1 = forms.CharField(
        label="Password",
        widget= forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Password'
            }),
    )
    password2 = forms.CharField(
        label="Password",
        widget= forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Confirm Password'
            }),
    )

    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Username'
            }),
            'email': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Email'
            }),
        }

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['username'].label = 'Display Name'
            self.fields['email'].label = "Emial Address"
            
class UserLoginForm(AuthenticationForm):    
        
        password = forms.CharField(
            label="Password",
            widget= forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Password'
            }),
        )
        class Meta:
            fields = ('username','email','password1','password2')
            model = get_user_model()
            widgets = {
                'username': TextInput(attrs={
                    'class': "form-control",
                    'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                    'placeholder': 'Username'
                }),
                'email': TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                    'placeholder': 'Email'
                }),
            }
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['username'].label = 'Display Name'
            self.fields['password'].label = "Password"
            
class UpdateFormView(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'width: 300px; text-align:center;  border-rounded: 25%; background:none; color:white',
                'placeholder': 'Title'
            })
        }