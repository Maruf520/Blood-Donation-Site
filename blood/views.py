from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Bank, Blood
from django.urls import reverse, reverse_lazy
from django import forms
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from cart.forms import CartAddBloodForm, CCartAddBloodForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect

decorators = [never_cache, login_required]


class BankListView(generic.ListView):
    model = Bank
    template_name = "bank/index.html"
    context_object_name = 'bank_list'


class BankDetailView(generic.DetailView):
    model = Bank
    template_name = "bank/detail.html"


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BloodCreateView(generic.CreateView):
    model = Blood
    template_name = "blood/blood_form.html"
    fields = ['group', 'description', 'price', 'stock', 'available']

    def get_queryset(self):
        queryset = super(BloodCreateView, self).get_queryset()
        bank_id = self.kwargs.get('pk')
        bank = Bank.objects.get(pk=bank_id)
        user = self.request.user
        if user.is_admin or user.is_superuser or user == bank.owner:
            return queryset
        else:
            return reverse('accounts:login')

    def form_valid(self, form):
        bank_id = self.kwargs.get('pk')
        # print(bank_id)
        form.instance.bank_id = bank_id
        group = form.cleaned_data.get('group')
        bank = Bank.objects.get(pk=bank_id)
        user = self.request.user
        if not (user.is_admin or user.is_superuser or user == bank.owner):
            return HttpResponse("Invalid Create Request")
        if group and Bank.objects.get(pk=bank_id).blood_set.filter(group=group).exists():
            return HttpResponse('Group has been already added. Try different One or Update existing one')
        # print(form.instance.group)
        # a = Bank.objects.get(pk=self.kwargs.get('pk'))
        # print(a.blood_set.all())
        # b = a.blood_set.all()
        # c = []

        # for blood in b:
        #     print(blood.group+" - slug -" + blood.slug)
        #     f = ''.join(blood.slug)
        #     c.append(f)
        #     print("c: ", c)
        #     if str(form.instance.slug) not in c:
        #         raise forms.ValidationError('Fuck You')
        return super(BloodCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blood:bank-list')


def blood_list(request, bank_slug=None):
    bank = None
    banks = Bank.objects.all()
    bloods = Blood.objects.filter(available=True)
    if bank_slug:
        bank = get_object_or_404(Bank, slug=bank_slug)
        bloods = Blood.objects.filter(bank=bank)

    context = {
        'bank': bank,
        'banks': banks,
        'bloods': bloods
    }
    print("Bank: ", bank)
    print("Banks: ", banks)
    print("bloods", bloods)
    return render(request, 'blood/list.html', context)


def blood_detail(request, id, slug):
    blood = get_object_or_404(Blood, id=id, slug=slug, available=True)

    maximum_quantity = blood.stock
    BLOOD_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, maximum_quantity)]

    cart_blood_form = CCartAddBloodForm(BLOOD_QUANTITY_CHOICES)
    context = {
        'blood': blood,
        'cart_blood_form': cart_blood_form
    }
    return render(request, 'blood/detail.html', context)




@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankCreateView(generic.CreateView):
    model = Bank
    template_name = "bank/bank-form.html"
    fields = ['name', 'location', 'logo', 'contact']

    def get_queryset(self):
        queryset = super(BankCreateView, self).get_queryset()
        user = self.request.user
        if user.is_admin or user.is_superuser:
            return queryset
        else:
            return redirect('../../../accounts/login/')

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        print(owner, owner.is_superuser)
        if owner.is_superuser or owner.is_admin:
            return super(BankCreateView, self).form_valid(form)
        else:
            return redirect('../../../accounts/login/')

    def get_success_url(self):
        return reverse('blood:bank-list')


# ###############
#  Bank update view
@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankUpdateView(generic.UpdateView):
    model = Bank
    fields = ['name', 'location', 'logo', 'contact']
    template_name_suffix = "_update_form"
    template_name = 'bank/bank_update_form.html'

    def get_queryset(self):
        queryset = super(BankUpdateView, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        print(owner, owner.is_superuser)
        if owner.is_superuser or owner.is_admin or owner.is_bank_owner:
            return super(BankUpdateView, self).form_valid(form)
        else:
            return redirect('../../accounts/login/')

    def get_success_url(self):
        return reverse('blood:bank-list')


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BankDeleteView(generic.DeleteView):
    model = Bank
    template_name = 'bank/bank_confirm_delete.html'
    success_url = reverse_lazy('blood:bank-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or self.request.user.is_admin or self.request.user.is_bank_owner or self.request.user.is_superuser:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseForbidden('Invalid Delete Request')


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BloodUpdateView(generic.UpdateView):
    model = Blood
    template_name_suffix = "_update_form"
    template_name = 'bank/bank_update_form.html'
    fields = ['bank', 'group', 'description', 'price', 'available', 'stock']
    # pk_url_kwarg = 'blood_pk'

    # def get_queryset(self):
    #     query_set = super(BloodUpdateView, self).get_queryset()
    #     query_set = query_set.filter(owner=self.request.user)
    #     query_set = query_set.filter(id=self.pk_url_kwarg)
    #     return query_set
    # def get_queryset(self):
    #     query_set = super(BloodUpdateView).get_queryset()
    #     print(query_set)
    #     return query_set
    def get_queryset(self):
        queryset = super(BloodUpdateView, self).get_queryset()
        queryset = queryset.filter(bank__owner=self.request.user)
        print("query set ", queryset)
        return queryset

    def form_valid(self, form):
        bank_id = self.kwargs.get('bank_pk')
        blood_id = self.kwargs.get('pk')
        print("blood_id", blood_id, "bank_id", bank_id)
        # print(bank_id)
        form.instance.id = blood_id
        # form.instance.bank_id = bank_id
        group = form.cleaned_data.get('group')
        # if group and Bank.objects.get(pk=bank_id).blood_set.filter(group=group).exists():
        #     return HttpResponse('Group has been already added. Try different One or Update existing one')
        return super(BloodUpdateView, self).form_valid(form)

        def get_success_url(self):
            return reverse('blood:bank-list')


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BloodDeleteView(generic.DeleteView):
    model = Blood
    template_name = 'bank/bank_confirm_delete.html'
    success_url = reverse_lazy('blood:bank-list')
    pk_url_kwarg = 'blood_pk'

    def get_queryset(self):
        queryset = super(BloodDeleteView, self).get_queryset()
        queryset = queryset.filter(bank__owner=self.request.user)
        if queryset == []:
            return HttpResponse("Invalid delete request")
        return queryset
