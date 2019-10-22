from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from blood_bank.forms import Bank_details_Form
from django import forms
from blood_bank.models import Bank_details, Blood_quantity

def BloodBankManage(request):
    if request.method == 'POST':
        
        bank_details_form = Bank_details_Form(request.POST, request.FILES)
        if bank_details_form.is_valid():
            bank_details_form.save()
            return HttpResponse('successful')
            # print(bank_details_form.errors)
            
        else:
            print(bank_details_form.errors)
            return HttpResponse('Error')
    else:
        bank_details_form = Bank_details_Form()

        context = {
            'bank_form': bank_details_form
        }
        return render(request, 'dashboard/blood_bank/blood_bank.html', context)       


def blood_banks_list(request ):
    if request.method == 'GET':
        banks = Bank_details.objects.all()

        context = {
            'banks': banks
        }
        return render(request, 'home/blood_bank/blood_banks_list.html', context)

def individual_bank (request, id):
    if request.method == 'GET':
        bank1 = Bank_details.objects.get(id=id)

        detail = Blood_quantity.objects.get(bank_id = id )
        context = {
            'bank':  bank1,
            'detail':detail
        }
        return render(request, 'home/blood_bank/individual_bank.html', context)
           

        #    '''
        #    Blood_quantity.objects.get(bank__owner=request.user)
        #    '''