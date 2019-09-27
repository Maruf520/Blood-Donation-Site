from django import forms
from  dashboard.models import Image

class SlidImageForm(forms.ModelForm):
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class':'form-control'}),
            # 'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
        }