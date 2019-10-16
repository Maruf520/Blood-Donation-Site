from django import forms
from blood_bank.models import Bank_details, Blood_quantity

class Bank_details_Form(forms.ModelForm):

    class Meta:
        model  = Bank_details
        fields = ['bank_name','bank_location', 'bank_logo','bank_contact','owner']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class':'form-control','placeholder':'location'}),
            'bank_location': forms.TextInput(attrs={'class':'form-control','placeholder':'bank_location'}),
            'bank_contact': forms.TextInput(attrs={'class':'form-control','placeholder':'bank_conatct'}),
            # 'owner': forms.TextInput(attrs={'class':'form-control','placeholder':'bank_conatct'}),
            'bank_logo': forms.FileInput(attrs={'class':'form-control'}),
        }

class Blood_quantity_form(forms.ModelForm):
    class Meta:
        model = Blood_quantity
        fields = ['ab_p', 'ab_n', 'a_p','a_n','b_p', 'b_n','o_p','o_n']
        widgets =  {
            'ab_p' : forms.NumberInput(attrs={'class': 'form-control'}),
            'ab_n' : forms.NumberInput(attrs={'class': 'form-control'}),
            'a_n' : forms.NumberInput(attrs={'class': 'form-control'}),
            'a_p' : forms.NumberInput(attrs={'class': 'form-control'}),
            'b_p' : forms.NumberInput(attrs={'class': 'form-control'}),
            'b_n' : forms.NumberInput(attrs={'class': 'form-control'}),
            'o_p' : forms.NumberInput(attrs={'class': 'form-control'}),
            'o_n' : forms.NumberInput(attrs={'class': 'form-control'}),
        }       


