# Create your views here.
import requests
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserRegisterForm, ShopRegisterForm
from django.core.mail import send_mail,EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.auth.models import User
from .models import Shop
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
import urllib.parse
from cart.models import Item

def mainRegister(request):
	return render(request, 'user/main_signup.html', {'users' : 1, 'shops': 2})

def mainLogin(request):
	return render(request, 'user/main_login.html')

def index(request):
	user = request.user
	num_items_in_cart=user.profile.cart_items.all().count()
	return render(request, 'home/navbar.html',{'num_items_in_cart':num_items_in_cart})


def activation_sent_view(request):
    return render(request, 'user/activation_sent.html')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	print(account_activation_token.check_token(user, token))
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.signup_confirmation = True
		user.save()
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return redirect('home:landing')
	else:
		return render(request, 'user/activation_invalid.html')


def register(request): 
	if request.method == 'POST':	
		form = UserRegisterForm(request.POST)
		print(form)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.email = form.cleaned_data.get('email')
			user.is_active = False
			user.user_type = 1
			user.save()
			current_site = get_current_site(request)
			print(current_site)
			subject = 'Please activate your Account'
			message = render_to_string('user/activation_request.html', {
				'user': user,
				'domain': '127.0.0.1:8000',
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			print(message)
			email = EmailMessage('email_subject', message, to=[user.profile.email])
			email.send()
			messages.success(request, "Your account has been created ! You are now able to log in")
			return redirect('user:activation_sent')
	else: 
		form = UserRegisterForm()
	return render(request, 'user/user_register.html', {'form': form, 'title':'reqister here'}) 


def registerShop(request):
	if request.method == 'POST':
		print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIii")	
		form = ShopRegisterForm(request.POST or None)
		print(form)
		if form.is_valid():
			user = form.save
			shop = Shop()
			print(user)
			# user.refresh_from_db()
			shop.username = form.cleaned_data['username']
			shop.set_password = form.cleaned_data['password1']
			shop.email = form.cleaned_data['email']
			shop.address = form.cleaned_data['address']
			shop.shop_name = form.cleaned_data['shop_name']
			shop.shop_registration_no = form.cleaned_data['shop_registration_no']
			shop.save()
			us = User.objects.create_user(username=shop.username,email=shop.email,password=shop.set_password)
			us.save()
			print(shop.address)

			# is_active = False
			shop.user_type = 2

			url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(shop.address) +'?format=json'
			response = requests.get(url).json()
			print(response[0]["lat"])
			print(response[0]["lon"])
			lat = response[0]["lat"]
			lon = response[0]["lon"]
			print(lat, lon)
			shop.latitude = lat
			shop.longitude = lon
			shop.save()
			
			current_site = get_current_site(request)
			subject = 'Please activate your Account'
			# message = render_to_string('user/activation_request.html', {
			# 	'user': user,
			# 	'domain': current_site.domain,
			# 	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			# 	'token': account_activation_token.make_token(user),
			# })
			# print(message)
			message = "Hello"
			email = EmailMessage('email_subject', message, to=[shop.email])
			email.send()
			messages.success(request, "Your account has been created ! You are now able to log in")
			return redirect('user:activation_sent')
	else: 
		form = ShopRegisterForm()
	return render(request,'user/shop_signup.html')
	# return render(request, 'user/shop_signup.html', {'form': form, 'title':'reqister here'})

def loginuser(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password1')
		print(username)
		print(password)
		user=authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			form=login(request, user)
			print(form)
			messages.success(request, f'Welcome {username} !!')
			user = request.user
			user.save()
			# print(user.profile.bio)
			return redirect('home:landing')
		else:
			messages.warning(request, "Such a user does not exist!!")
			# return redirect('user:register')
	form=AuthenticationForm()

	return render(request, 'user/user_login.html', {'form':form, 'title':'log in'})


# def Login(request):
# 	if request.method=="POST":
# 		username=request.POST.get('username')
# 		password=request.POST.get('password1')
# 		print(username)
# 		print(password)
# 		user=authenticate(request, username=username, password=password)
# 		print(user)
# 		if user is not None:
# 			form=login(request, user)
# 			print(form)
# 			messages.success(request, f'Welcome {username} !!')
# 			user = request.user
# 			user.save()
# 			# print(user.profile.bio)
# 			return redirect('home:landing')
# 		else:
# 			messages.warning(request, "Such a user does not exist!!")
# 			# return redirect('user:register')
# 	form=AuthenticationForm()

# 	return render(request, 'user/user_login.html', {'form':form, 'title':'log in'})


def LoginShop(request):
	if request.method=="POST":
		username = request.POST.get('username')
		registration_no = request.POST.get("shop_registration_no")
		password = request.POST.get('password1')
		user=authenticate(request, username=username, password=password)
		if user is None:
			print("Wrong User")
			messages.warning(request, "Wrong credentials or Invalid User")
		else:
			flag=0
			if Shop.objects.filter(shop_registration_no=registration_no):
				flag = 1
			form = login(request,user, backend='django.contrib.auth.backends.ModelBackend')
			print(form)
			all_items = Item.objects.all()
			return render(request, 'cart/shop_dash.html', {'all_items': all_items})

	return render(request, 'user/shop_login.html')

def profilepage(request):
	user=request.user
	all_items = user.profile.cart_items.all()
	num_items_in_cart = all_items.count()
	# print(all_items)
	context = {'all_items':all_items, 'num_items_in_cart':num_items_in_cart}
	return render(request, 'user/profile.html', context)