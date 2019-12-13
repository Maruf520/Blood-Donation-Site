from django.shortcuts import render, redirect
from . import views
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages, auth
from django.contrib.auth import login as login_dj, logout, authenticate
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, SigninForm, ProfleUpdateForm, Password_reset_email_form, Password_verification_form
from django.http import HttpResponse
from accounts.models import Account
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User
from misc.token import token_decode, token_encode
from django.core.mail import send_mail
from post.models import Blog
from django.views.decorators.cache import never_cache
from cart.cart import Cart


def send_password_reset_token(token, email):
    send_mail('Verification Token : ', token, 'md.maruf5201@gmail.com', [email],
              fail_silently=False)


def login(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.user
            login_dj(request, user)
            # if request.user.is_admin == True:

            #     details = Blood_quantity.objects.get(bank__owner=request.user)
            #     context  ={
            #         'detail':details
            #     }
            #     return render (request,)

            return redirect('/')

    else:
        form = SigninForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


@never_cache
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
    cart = Cart(request)
    cart.clear()
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/signin/')
def User_Profile(request):
    if request.method == 'GET':
        post = Blog.objects.filter(user_id=request.user)
        post_number = Blog.objects.filter(user_id=request.user).count()
        # Total_donation = Account.objects.filter(user=request.user).count()
        print(post_number)
        context = {
            'posts': post,
            'post_number': post_number,
            # 'Total_donation':Total_donation,
        }
        return render(request, 'home/profile/profile.html', context)


@login_required(login_url='/signin/')
def profile_update(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = ProfleUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfleUpdateForm(user=user)
        context = {
            'form': form
        }
        return render(request, 'home/profile/profile_update_form.html', context)


def password_reset(request):
    if request.method == 'GET':
        form = Password_reset_email_form()
        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset/password_reset_email.html', context)

    if request.method == 'POST':
        form = Password_reset_email_form(request.POST)
        if form.is_valid():
            # check whether any account exists or not with this email
            email = form.cleaned_data['email']
            try:
                account = Account.objects.get(email__iexact=email)
                data = {
                    'user_id': account.id,
                    'email': account.email
                }
                token = token_encode(data)
                print(token)
                send_password_reset_token(token, account.email)

                return redirect('confirm_passwword')
            except ObjectDoesNotExist:
                pass

    return HttpResponse("ERROR")


def confirm_password(request):
    if request.method == 'POST':
        form = Password_verification_form(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            data = token_decode(token)
            if data:
                account = Account.objects.get(id=data['user_id'])
                account.set_password(form.cleaned_data['password'])
                account.save()
                return HttpResponse('password changed')
    form = Password_verification_form()
    context = {
        'form': form
    }
    return render(request, 'accounts/password_reset/confirm_password.html', context)
