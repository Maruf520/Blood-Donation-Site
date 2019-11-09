from django.shortcuts import render
from django.views import generic
from .models import Bank, Quantity
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankListView(generic.ListView):
    model = Bank
    template_name = "bank/bank-form.html"
    context_object_name = 'bank_list'

    def get_queryset(self):
        queryset = super(BankListView, self).get_queryset()
        queryset = Bank.objects.all()
        return queryset
