from django import forms
from django.contrib.auth import authenticate
from accounts.models import Account

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



class SignupForm(forms.ModelForm):
	password  = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'password (min 6 word)','class':'form-control','minLength':'5', 'maxLength':'10' }))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'confirm_password', 'class': 'form-control'}))
	blood_group = forms.CharField( widget=forms.Select( choices=blood_type , attrs={'class':'custom-select'}))
	last_date_of_donation = forms.DateField(widget=forms.DateInput(attrs = {'placeholder':'date', 'class': 'form-control','type':'date'}))
	class Meta:
		model = Account
		fields = ['email','phone','blood_group','address', 'username']
		widgets = {
			'username' : forms.TextInput(attrs={'class':'form-control'}),
			
			'email' : forms.EmailInput(attrs={ 'class': 'form-control' }),
			'phone' : forms.TextInput(attrs={'class':'form-control'}),
			'address' : forms.TextInput(attrs={'class':'form-control'}),
			
		} 
	def email(self):
			email = self.cleaned_data['email']
			query =  Account.objects.filter(email = email)
			if query.exists():
				raise forms.ValidationError(' Email has already registered')
			return email    


	def phone(self):
			phone = self.cleaned_data['phone']
			query =  Account.objects.filter(phone = phone)
			if query.exists():
				raise forms.ValidationError(' This number  has already registered')
			return phone    
	def clean_confirm_password(self):
			password = self.cleaned_data['password']
			confirm_password = self.cleaned_data['confirm_password']
			if len(password) < 7:
				raise forms.ValidationError(' 7 length')
			if len(password) > 12:
				raise forms.ValidationError('password should be at most 12 length')
			# if not any(char.isdigit() for char in password):
			#     raise forms.ValidationError('password must contain at least 1 digit')
			# if not any(char.isupper() for char in password):
			#     raise forms.ValidationError('password must contain at least 1 upper letter')
			# if not any(char.islower() for char in password):
			#     raise forms.ValidationError('password must contain at least 1 upper letter')
			# if not any(symbol in password for symbol in ['~','!','#','$']):
			#     raise forms.ValidationError("use any of '~','!','#','$'")
			if not password or not confirm_password or password != confirm_password:
				raise forms.ValidationError('passwords are not matched')
			return confirm_password
	def save(self, commit = True):
			user = Account(
			username = self.cleaned_data['username'],
			email = self.cleaned_data['email'],
			phone = self.cleaned_data['phone'],
			blood_group = self.cleaned_data['blood_group'],
			address = self.cleaned_data['address'],
			last_date_of_donation = self.cleaned_data['last_date_of_donation']

			)         
			user.set_password(self.cleaned_data['confirm_password'])
			if commit:
				user.save()
			return user   
class SigninForm(forms.Form):
	email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control'}))
	password = forms.CharField(max_length=12, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))

	def clean(self):
		cleaned_data = self.cleaned_data
		email = cleaned_data['email']
		password = cleaned_data['password']
		db_user = Account.objects.filter(email__iexact=email).first()
		if not db_user:
			raise forms.ValidationError("invalid user")
		user = authenticate(username=db_user.username, password=password)
		if user:
			self.user = user
			return cleaned_data
		raise forms.ValidationError('invalid information')
class Password_reset_email_form(forms.Form):
		email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control'}))

class Password_verification_form(forms.Form):
	token = forms.CharField(widget=forms.TextInput(attrs = {'placeholder':'Enter Your Token', 'class': 'form-control'}))
	
	password  = forms.CharField(widget=forms.PasswordInput(
		attrs={ 'placeholder': 'password (min 6 word)','class':'form-control','minLength':'6', 'maxLength':'10' }))
	confirm_password  = forms.CharField(widget=forms.PasswordInput(
		attrs={ 'placeholder': 'password (min 6 word)','class':'form-control','minLength':'6', 'maxLength':'10' }))

	def clean_confirm_password(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		if len(password) < 6:
			raise forms.ValidationError('password should be at least 6 length')
		if len(password) > 12:
			raise forms.ValidationError('password should be at most 12 length')
		# if not any(char.isdigit() for char in password):
		#     raise forms.ValidationError('password must contain at least 1 digit')
		# if not any(char.isupper() for char in password):
		#     raise forms.ValidationError('password must contain at least 1 upper letter')
		# if not any(char.islower() for char in password):
		#     raise forms.ValidationError('password must contain at least 1 upper letter')
		# if not any(symbol in password for symbol in ['~','!','#','$']):
		#     raise forms.ValidationError("use any of '~','!','#','$'")
		if not password or not confirm_password or password != confirm_password:
			raise forms.ValidationError('passwords are not matched')
		return confirm_password

class ProfleUpdateForm(forms.ModelForm):
	blood_group = forms.CharField( widget=forms.Select( choices=blood_type , attrs={'class':'custom-select'}))
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
			'image': forms.FileInput(attrs={'class':'form-control'}),
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
		self.user = kwargs.pop('user', None)

		super(ProfleUpdateForm, self).__init__(*args, **kwargs)		

		self.fields['username'].initial = self.user.username
		self.fields['phone'].initial = self.user.phone
		self.fields['email'].initial = self.user.email
		self.fields['address'].initial = self.user.address
		self.fields['blood_group'].initial = self.user.blood_group
		self.fields['last_date_of_donation'].initial = self.user.last_date_of_donation
		# self.fields['image'].initial = self.user.image
		
