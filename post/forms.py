from django import forms
from post.models import Comment,Blog
from django.core.validators import RegexValidator


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
            'quantity' : forms.NumberInput(attrs={'max':4, 'min':1 ,'class':'form-control','placeholder':'1 (bag)'})
        }
    	# def clean_quantity(self):

        #     quantity = self.cleaned_data['quantity']
        #     if len(quantity) > 4:
        #         raise forms.ValidationError('quantity should be maximum 4')
        #     return quantityy


    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(BloodPostForm, self).__init__(*args, **kwargs)
        
        if user:
            if user.is_authenticated:
                self.fields['phone'].initial = user.phone
                self.fields['name'].initial = user.username
                self.user = user
        else:
            self.user = None

    def save(self, commit=True):
        blog  = Blog()
        blog.blood_group = self.cleaned_data['blood_group'] 
        blog.description = self.cleaned_data['description'] 
        blog.phone = self.cleaned_data['phone'] 
        blog.date = self.cleaned_data['date'] 
        blog.time = self.cleaned_data['time'] 
        blog.name = self.cleaned_data['name'] 
        blog.location = self.cleaned_data['location'] 
        blog.quantity = self.cleaned_data['quantity'] 
        # if self.user:
        blog.user = self.user

        if commit:
            blog.save()
        return blog    
            

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.TextInput(attrs = {'class' : 'form-control z-depth-1','placeholder': 'Enter Your Comment'})
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        post = kwargs.pop('post', None)
        super(CommentPostForm, self).__init__(*args, **kwargs) 
        self.user = user
        self.post = post

    def save(self, commit=True):
        comment = Comment()
        comment.text = self.cleaned_data['text']
        comment.user = self.user
        comment.blog = self.post
        if commit:
            comment.save()
        return comment
       