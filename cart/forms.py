from django import forms
from blood.models import Blood

BBLOOD_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CCartAddBloodForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=(), coerce=int)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        print("clean", self.cleaned_data, "quantity", quantity)
        if(quantity > 3):
            raise forms.ValidationError("Error!")

    def __init__(self, BLOOD_QUANTITY_CHOICES=[(i, str(i)) for i in range(1, 26)], *args, **kwargs):
        # blood_id = kwargs.pop("blood_id")
        super(CCartAddBloodForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].choices = BLOOD_QUANTITY_CHOICES


class CartAddBloodForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=(BBLOOD_QUANTITY_CHOICES), coerce=int)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        print("hello")
        super(CartAddBloodForm, self).__init__(*args, **kwargs)
