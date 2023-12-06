from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import *




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'testapp/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'testapp/register.html', {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request,'testapp/profile.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'testapp/login.html', {'form': form})

def home(request):
    return render(request, 'testapp/home.html')

def profile(request):
    if request.user.is_authenticated:
        return render(request,'testapp/profile.html')
    else:
        return HttpResponse('Invalid login')
    
def home1(request):
    if request.method == 'POST':
        home1 = MainPage(request.POST)
        return render(request,'testapp/profile.html')
    else:
        home1 = MainPage()
    return render(request, 'testapp/login.html', {'home1': home1})



