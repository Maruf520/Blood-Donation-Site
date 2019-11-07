from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/', views.User_Profile, name='profile'),
    path('password/reset', views.password_reset, name='forget_password'),
    path('password/token/verify', views.confirm_password, name='confirm_passwword'),


]
