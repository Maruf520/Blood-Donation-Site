from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/created/', views.thank_giving, name= 'thank-giving'),
]
