from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли отличаются')
        return cd['password2']
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MainPage(forms.Form):
    num = forms.CharField(label="Введите номер лабораторной работы")    
    num_ch = forms.CharField(label="Количество разделов")
    


class CharapterBaseForm(forms.Form):
    charapter = forms.CharField()
    text = forms.CharField()
    #images = forms.CharField()

def FormSet(num_ch):
    CharapterFormSet = formset_factory(CharapterBaseForm, extra=num_ch)
    return CharapterFormSet
