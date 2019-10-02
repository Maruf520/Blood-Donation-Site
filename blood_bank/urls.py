from django.urls import path
from . import views
urlpatterns = [
    
    path('add/account/', views.BloodBankManage, name='BloodBankManage'),
    path('blood_bank_list/', views.blood_banks_list, name='blood_banks'),
    path('blood_bank_list/individual_bank/<int:id>', views.individual_bank, name='individual_bank'),
    
]