from django.urls import path, include
from django.conf import settings
from . import views
from user import views as user_view
from django.contrib.auth import views as auth
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    # path('', views.index, name ='index'),
    # path('login/', user_view.Login, name='login'),
    path('loginuser/', user_view.loginuser, name='loginuser'),
    path('loginshop/', user_view.LoginShop, name='loginshop'),
    path('profile/', user_view.profilepage, name='profile'),
    path('logout/', auth.LogoutView.as_view(template_name='home/landingpage1.html'), name='logout'),
    path('mainregister/', user_view.mainRegister, name='mainRegister'),
    path('mainlogin/', user_view.mainLogin, name='mainLogin'),
    path('register/', user_view.register, name='register'),
    path('registerShop/', user_view.registerShop, name='registerShop'),
    path('user/sent/', user_view.activation_sent_view, name="activation_sent"),
    path('user/activate/<slug:uidb64>/<slug:token>/', user_view.activate, name='activate'),
    # url('^', include('django.contrib.auth.urls')),
    # path('accounts/', include('allauth.urls')),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name ='user/password_reset_form.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm')
]
