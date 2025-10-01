from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from users.forms import LoginForm, SignupForm, RevisionForm

from users.models import User


def user_index(request):
    return render(request, 'base.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


# Create your views here.

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                    return render(request, 'signup.html', {'form': form})

                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Passwords do not match')
                    return render(request, 'signup.html', {'form': form})

                user = User.objects.create_user(username=username,password=password1)
                user = authenticate(username=username, password=password1)

                login(request, user)
                return redirect('/')
        else:
            form = SignupForm()
    context = {'form' : form}
    return render(request, 'signup.html', context)

def user_info(request):
    return render(request, 'userInfo.html')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next') or request.POST.get('next') or '/'
                return redirect(next_url)
            else:
                messages.error(request, 'Username OR password is incorrect')
                #form.add_error(None, 'Not a valid username or password.')
    else:
        form = LoginForm()
    context = {
        'form' : form,
        'next' : request.GET.get('next', '/') # 이게 없으면 안되네
    }
    return render(request, 'login.html', context)

def user_edit(request):
    user = request.user
    form = RevisionForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/users/userinfo/")
    else:
        pass



