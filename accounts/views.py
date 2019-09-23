from django.shortcuts import render, redirect
from . import views
from django.contrib import messages, auth
from django.contrib.auth import login as login_dj, logout, authenticate
from accounts.forms import SignupForm,SigninForm
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
		'form' : form
	}

	return render(request, 'accounts/login.html', context) 


def register(request):

	context = {}
	if request.method == 'POST':
		form = SignupForm( request.POST )
		
		if form.is_valid():
			user = form.save()
			user.save()
			return redirect( 'login')

	else:
		form = SignupForm()
	context = {
		'form' : form
	}
	return render( request, 'accounts/register.html', context )
# @login_required(login_url='/login')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')	
	