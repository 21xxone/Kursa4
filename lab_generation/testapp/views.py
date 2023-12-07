from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, MainPage, CharapterBaseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.forms import formset_factory
from .replace import *
from .writeToDocx import *

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
    
def generalInfo(request):
    if request.method == 'POST':
        generalInfo = MainPage(request.POST)
        if (int(request.POST.get('num_ch', '')) > 10 or int(request.POST.get('num_ch', '')) < 1):
            return render(request, 'testapp/generalInfo.html', {'generalInfo': generalInfo})
        else:
            #fill docx#
            keyword_dict["[num]"] = request.POST.get('num', '')
            keyword_dict["[group]"] = request.POST.get('group', '')
            keyword_dict["[username]"] = request.POST.get('fio', '')
            keyword_dict["[username1]"] = request.POST.get('fio2', '')
            keyword_dict["[mission]"] = request.POST.get('mission', '')
            request.session['num_ch'] = request.POST.get('num_ch', '')
            request.session['conclusion'] = request.POST.get('conclusion', '')
            checkIfExists()
            replace()
            return redirect('/chapterInfo')
    else:
        generalInfo = MainPage()
        return render(request, 'testapp/generalInfo.html', {'generalInfo': generalInfo})


def chapterInfo(request):
    num_ch = request.session['num_ch']
    ChapterInfoSet = formset_factory(CharapterBaseForm, extra=int(num_ch))

    if request.method == 'POST':
        newOut()
        chapterset = ChapterInfoSet(request.POST)
        for f in chapterset:
            writeToDocx(f['charapter'].value(), True)
            writeToDocx(f['text'].value(), False)
        #fill docx#
        writeToDocx("Вывод", True)
        writeToDocx(request.session['conclusion'], False)
        return render(request,'testapp/profile.html')
    else:
        context = {}
        chapterset = ChapterInfoSet()
        context['chapterSet'] = chapterset
        return render(request, 'testapp/chapterInfo.html', context)
