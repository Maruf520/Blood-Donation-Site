from django import forms
from  dashboard.models import Image,Commttee,Gallery,Report
from  accounts.models import Account

blood_type = (
	('AB+', 'AB+'),
	('A+','A+'),
	('AB-', 'AB-'),
	('O+','O+'),
	('O-','O-'),
	('A-','A-'),
	('B+','B+'),
	('B-','B-')
)


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


class GalleryImageForm(forms.ModelForm):
	# image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
	class Meta:
		model = Gallery
		fields = ['image']
		widgets = {
			'image': forms.FileInput(attrs={'class':'form-control'}),
			# 'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
		}

class AccountUpdateForm(forms.ModelForm):
	
	blood_group = forms.CharField( widget=forms.Select( choices=blood_type , attrs={'class':'custom-select'}))
	image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
	class Meta:
		model = Account
		fields = ['username','email','phone','address','blood_group','last_date_of_donation','image']
		widgets = {
		'username' : forms.TextInput(attrs={
				'placeholder' : 'Username', 'class' : 'form-control', 'style' : 'color: black'
				}),
			'email' : forms.TextInput(attrs={
				'placeholder' : 'Email', 'class' : 'form-control'
				}),
			'phone' : forms.TextInput(attrs={
				'placeholder' : 'Phone', 'class' : 'form-control'
				}),
			'blood_group' : forms.TextInput(attrs={
				'placeholder' : 'Blood Group', 'class' : 'form-control'
				}),
			'address' : forms.TextInput(attrs={
				'placeholder' : ' Address', 'class' : 'form-control'
				}),

				'last_date_of_donation' : forms.DateInput(format='%d-%m-%Y',attrs={'class' : 'form-control','type':'date' }),
			
		}

	def clean(self):
		cleaned_data = self.cleaned_data
		phone = cleaned_data['phone']
		email = cleaned_data['email']
		username = cleaned_data['username']
		blood_group = cleaned_data['blood_group']
		address = cleaned_data['address']
		last_date_of_donation = cleaned_data['last_date_of_donation']
		image = cleaned_data['image']
		# valid = self.user.check_password(password)
		# if not valid:
		# 	raise forms.ValidationError('invalid password')

		duplicate_email = Account.objects.filter(email=email).exclude(id=self.user.id)
		if duplicate_email.exists():
			raise forms.ValidationError('This email is already registered')

		duplicate_phone = Account.objects.filter(phone=phone).exclude(id=self.user.id)
		if duplicate_phone.exists():
			raise forms.ValidationError('This phone is already registered')

		return cleaned_data
	
	def is_new_email(self):
		if self.user.email.lower() != self.cleaned_data.get('email').lower():
			return False
		return True


	def save(self, commit=True):
		username = self.cleaned_data['username']
		email = self.cleaned_data['email']
		address = self.cleaned_data['address']
		phone = self.cleaned_data['phone']
		blood_group = self.cleaned_data['blood_group']
		last_date_of_donation = self.cleaned_data['last_date_of_donation']
		image = self.cleaned_data['image']

		self.user.username = username
		self.user.phone = phone
		self.user.email = email
		self.user.address = address
		self.user.blood_group = blood_group
		self.user.last_date_of_donation = last_date_of_donation
		self.user.image = image

		if commit:
			self.user.save()
		return self.user        
		
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(AccountUpdateForm, self).__init__(*args, **kwargs)
		self.user = user
		self.fields['username'].initial = user.username
		self.fields['phone'].initial = user.phone
		self.fields['email'].initial = user.email
		self.fields['address'].initial = user.address
		self.fields['blood_group'].initial = user.blood_group
		self.fields['last_date_of_donation'].initial = user.last_date_of_donation

class ReportForm(forms.ModelForm):
	class Meta :
		model = Report
		fields = ['messege']
		widgets = {
			'messege': forms.TextInput(attrs={'class':'form-control','placeholder':'For any complane'}),
		}