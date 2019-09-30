from django.shortcuts import render,HttpResponse,redirect
from blood_bank.forms import Bank_details_Form

def BloodBankManage(request):
    if request.method == 'POST':
        bank_details_form = Bank_details_Form(request.POST)
        if bank_details_form.is_valid():
            bloodBank = bank_details_form.save()
            print(bloodBank)
            return HttpResponse('fuck')
        
    else:
        bank_details_form = Bank_details_Form()

        context = {
            'bank_form': bank_details_form
        }
        return render(request, 'dashboard/blood_bank/blood_bank.html', context)       



# Create your views here.
