"""AucSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.Home, name='Home'),
    path('Auc_Page', views.Auc_Page, name='Auc_Page'),
    path('auctionRegister/<p_id>/', views.auctionRegister, name='auctionRegister'),
    path('handleRegisterForm',views.handleRegisterForm, name='handleRegisterForm'),
    path('Signup',views.Signup, name='Signup'),
    path('handleSignup',views.handleSignup, name='handleSignup'),
    path('Login', views.Login, name='Login'),
    path('handleLogin',views.handleLogin, name='handleLogin'),
    path('forgotPwd', views.forgotPwd, name='forgotPwd'),
    path('handleForgotPwd', views.handleForgotPwd, name='handleForgotPwd'),
    path('Logout', views.log_out, name='log_out'),
    path('Profile',views.profile, name='profile'),
    path('sellProduct', views.sellProduct, name='sellProduct'),
    path('handleSellProd', views.handleSellProd, name='handleSellProd'),
    path('Contact_Us',views.Contact_Us, name='Contact_Us'),
    path('handleContactUs', views.handleContactUs, name='handleContactUs'),
    path('About_Us',views.About_Us, name='About_Us'),
    path('TnC',views.TnC, name='TnC'),
    path('ajax/getUsers/<Product_id>/',views.getUsers,name='getUsers'),
    path('', views.index, name='index'),
    path('facecam_feed/<p_id>', views.facecam_feed, name='facecam_feed'),
    path('endAuction/<p_id>',views.endAuction,name='endAuction'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)