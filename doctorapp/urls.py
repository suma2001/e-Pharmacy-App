"""doctorapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from user import views as user_view
from django.contrib.auth import views as auth_views

# app_name = 'doctorapp'

urlpatterns = [

    path('admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),

    # path('accounts/', include('allauth.urls')),
    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(
    #          template_name='user/password_reset.html'
    #      ),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='user/password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='user/password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    ##### user related path#########################
    path('user/', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls')),
    path('', include('home.urls')),
    # path('', include('django.contrib.auth.urls'))

]
