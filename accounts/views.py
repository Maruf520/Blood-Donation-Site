from django.shortcuts import render, redirect
from . import views
from django.contrib import messages, auth
from django.contrib.auth import login as login_dj, logout, authenticate
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, SigninForm, ProfleUpdateForm
from django.http import HttpResponse
from accounts.models import Account
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect('register')
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.user
            login_dj(request, user)
            return redirect('/')

    else:
        form = SigninForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def register(request):

    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('login')

    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
# @login_required(login_url='/login')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/signin/')
def User_Profile(request):
    if request.method == 'GET':

        context = {
            'user': request.user
        }
        return render(request, 'dashboard/userprofile/userprofile.html', context)

# def User_Profile1(request):
# 	if request.method == 'GET':
# 		user = Account.objects.all()
# 		print(user)
# 		context = {
# 			'users' : user
# 		}
# 		return render (request, 'home/partials/menu_area.html', context)
#


@login_required(login_url='/signin/')
def update(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = ProfleUpdateForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfleUpdateForm(user=user)
        context = {
            'form': form
        }
        return render(request, 'dashboard/userprofile/profile_update_form.html', context)
