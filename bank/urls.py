from django.urls import include, path
from .models import Bank
from .import views
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
app_name = 'bank'


urlpatterns = [
    path('', views.BankListView.as_view(), name='bank-index'),
    path('create_bank/', views.BankCreateView.as_view(), name='bank-create'),
    path('update_bank/<int:pk>/',
         login_required(views.BankUpdateView.as_view()), name='bank-update'),
    path('delete/<int:pk>/',
         views.BankDeleteView.as_view(), name='bank-delete'),
]
