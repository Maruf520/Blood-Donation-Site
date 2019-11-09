from django.urls import include, path
from .models import Bank, Quantity
from .import views
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
app_name = 'bank'


urlpatterns = [
    path('', views.BankListView.as_view(), name='bank-index'),
]
