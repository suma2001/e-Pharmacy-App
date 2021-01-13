from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from .models import Shop

class UserRegisterForm(UserCreationForm): 
	email = forms.EmailField() 
	phone_no = forms.CharField(max_length = 20) 
	# first_name = forms.CharField(max_length = 20) 
	# last_name = forms.CharField(max_length = 20) 
	class Meta: 
		model = User 
		fields = ['username', 'email', 'phone_no', 'password1', 'password2'] 

class ShopRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=50)
	password1 = forms.CharField(max_length=20)
	password2 = forms.CharField(max_length=20)
	email = forms.EmailField()
	address = forms.CharField(max_length=250)
	phone_no = forms.CharField(max_length = 20)
	shop_name = forms.CharField(max_length = 50)
	shop_registration_no = forms.CharField(max_length = 30)

	class Meta:
		model = Shop
		fields = ['username', 'email', 'phone_no','address','password1', 'password2', 'shop_name', 'shop_registration_no']
