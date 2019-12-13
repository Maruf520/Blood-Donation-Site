from django.urls import path, include
from .models import Bank, Blood
from . import views

app_name = 'blood'


urlpatterns = [
    path('update-bank/<int:pk>/', views.BankUpdateView.as_view(), name='bank-update'),
    path('bank/create/', views.BankCreateView.as_view(), name='bank-create'),
    path('', views.BankListView.as_view(), name='bank-list'),
    path('details/<int:pk>/', views.BankDetailView.as_view(), name='bank-detail'),
    path('bank/<int:pk>/create/',
         views.BloodCreateView.as_view(), name='blood-create'),
    path('<slug:bank_slug>/', views.blood_list, name='blood_list_by_bank'),
    path('<int:id>/<slug:slug>/', views.blood_detail, name='product_detail'),
    path('bank/delete/<int:pk>/', views.BankDeleteView.as_view(), name='bank-delete'),
    path('bank/<int:bank_pk>/blood/<int:pk>/',
         views.BloodUpdateView.as_view(), name='blood-update'),
    path('bank/<int:pk>/blood/<int:blood_pk>/delete/',
         views.BloodDeleteView.as_view(), name='blood-delete'),
    path('search/', views.SearchView, name='bank-search'),
]
