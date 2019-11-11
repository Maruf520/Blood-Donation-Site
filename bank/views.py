from django.shortcuts import render
from django.views import generic
from .models import Bank, Quantity
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankListView(generic.ListView):
    model = Bank
    template_name = "bank/bank-index.html"
    context_object_name = 'bank_list'

    def get_queryset(self):
        queryset = super(BankListView, self).get_queryset()
        queryset = Bank.objects.all()
        return queryset


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankCreateView(generic.CreateView):
    model = Bank
    template_name = "bank/bank-form.html"
    fields = ['name', 'location', 'logo', 'contact']

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        print(owner, owner.is_superuser)
        if owner.is_superuser or owner.is_admin or owner.is_bank_owner:
            return super(BankCreateView, self).form_valid(form)
        else:
            return redirect('../../accounts/login/')

    def get_success_url(self):
        return reverse('bank:bank-index')


class BankUpdateView(generic.UpdateView):
    model = Bank
    fields = ['name', 'location', 'logo', 'contact']
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        print(owner, owner.is_superuser)
        if owner.is_superuser or owner.is_admin or owner.is_bank_owner:
            return super(BankUpdateView, self).form_valid(form)
        else:
            return redirect('../../accounts/login/')

    def get_success_url(self):
        return reverse('bank:bank-index')


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankDeleteView(generic.DeleteView):
    model = Bank
    template_name = 'bank/bank_confirm_delete.html'
    success_url = reverse_lazy('bank:bank-index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or self.request.user.is_admin or self.request.user.is_bank_owner or self.request.user.is_superuser:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden('Invalid Delete Request')
