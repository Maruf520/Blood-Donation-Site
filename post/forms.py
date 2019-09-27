from django import forms
from post.models import Comment,Blog



class BloodPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['blood_group', 'quantity', 'location', 'description',
        'phone', 'date', 'time', 'name']    
        widgets = {
            'location' : forms.TextInput(attrs={'class':'form-control','placeholder':'location'}),
            'description' : forms.Textarea(attrs={'class':'form-control','placeholder':'description'}),
            'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
            'date' : forms.DateInput(attrs={'class':'form-control','placeholder':'date','type':'date'}),
            'time' : forms.TimeInput(attrs={'class':'form-control','placeholder':'time', 'type':'time'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control','placeholder':'name'}),
            'blood_group' : forms.Select(attrs={'class':'form-control','placeholder':'blood_group'}),
            'quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'quantity'})
        }



    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(BloodPostForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['phone'].initial = user.phone
            self.fields['name'].initial = user.username

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.TextInput(attrs = {'class' : 'form-control z-depth-1','placeholder': 'Enter Your Comment'})
        }
