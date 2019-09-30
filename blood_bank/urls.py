from django.urls import path
from . import views
urlpatterns = [
    
    path('add/account/', views.BloodBankManage, name='BloodBankManage')
    
]