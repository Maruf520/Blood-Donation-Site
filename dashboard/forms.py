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

class DropDownForm(forms.Form):
    session = forms.ModelChoiceField( queryset=Commttee.objects.values_list("session", flat=True).distinct(),
    )
class CommitteeEditForm(forms.ModelForm):
    class Meta:
        model = Commttee
        fields = ['name','designation','session','image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'john doe'}),
            'designation': forms.TextInput(attrs={'class':'form-control','placeholder':'john doe'}),
            'session': forms.TextInput(attrs={'class':'form-control','placeholder':'john doe'}),
        }
    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data['name']
        designation = cleaned_data['desigantion']
        session = cleaned_data['session']
        image = cleaned_data['image']

    def save(self, commit=True):
        name = self.cleaned_data['name']
        designation = self.cleaned_data['designation']
        session = self.cleaned_data['session']
        image = self.cleaned_data['image']
        self.user.name = name
        self.user.designation = designation
        self.user.session = session
        self.user.image = image

        if commit:
            self.user.save()
        return self.user

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(CommitteeEditForm, self).__init__(*args, **kwargs)		

        self.fields['name'].initial = self.user.name
        self.fields['designation'].initial = self.user.designation
        self.fields['session'].initial = self.user.session
        self.fields['image'].initial = self.user.image    


# class CommitteeEditForm(forms.ModelForm):
#     class Meta:
#         model : Commttee
#         fields : ['name','desigantion','session','image']
#         widgets = {
#             'name' : forms.TextInput(attrs={'class' : 'form-control'}),   
#             'designation' : forms.TextInput(attrs={'class' : 'form-control'}),  
#             'sesssion' : forms.TextInput(attrs={'class' : 'form-control'}),  
#             'image' : forms.TextInput(attrs={'class' : 'form-control'}),           
#          }
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     name = cleaned_data['name']
    #     designation = cleaned_data['desigantion']
    #     session = cleaned_data['session']
    #     image = cleaned_data['image']

    # def save(self, commit=True):
    #     name = self.cleaned_data['name']
    #     designation = self.cleaned_data['designation']
    #     session = self.cleaned_data['session']
    #     image = self.cleaned_data['image']
    #     self.user.designation = designation
    #     self.user.session = session
    #     self.user.image = image

        # if commit:
        #     self.user.save()
        # return self.user

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)

    #     super(CommitteeEditForm, self).__init__(*args, **kwargs)		

    #     self.fields['name'].initial = self.user.name
    #     self.fields['designation'].initial = self.user.designation
    #     self.fields['session'].initial = self.user.session
    #     self.fields['image'].initial = self.user.image
        
                


