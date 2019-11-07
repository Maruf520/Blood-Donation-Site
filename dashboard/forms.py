from django import forms
from  dashboard.models import Image,Commttee

class SlidImageForm(forms.ModelForm):
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class':'form-control'}),
            # 'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
        }

class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Commttee
        fields = ['name','designation','session','image']        
        widgets  = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'john doe'}),
            'designation':forms.TextInput(attrs={'class':'form-control','placeholder':'president'}),
            'session': forms.DateTimeInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),

         }