from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from Home.models import Client, Registered_Users, Product
from AucPage.models import Auction
import re, os

# Create your views here.




def handleEnterForm(request):
    if request.method=="POST":
        error=[]
        aucFormUname = request.POST['aucFormUname']
        aucFormCode = request.POST['aucFormCode']
        try:
            client_obj = Client.objects.get(Uname=aucFormUname)
        except:
            error.append("Invalid Username!")
        try:
            reg_user_obj = Registered_Users.objects.get(User_Name=aucFormUname,PassCode=aucFormCode)
        except:
            error.append("User not Registered!")
        try:
            product_obj = Product.objects.get(id=reg_user_obj.Product_ID, Auction_Passcode=aucFormCode)
        except:
            error.append('Invalid User or Passcode!')
        if not error:
            try:
                check=Auction.objects.get(ClientUsername=reg_user_obj.User_Name, ProductID=product_obj.id)
            except:
                auc_obj = Auction(OwnerName=reg_user_obj.Product_Owner, ProductID=product_obj.id, ClientUsername=reg_user_obj.User_Name, ClientID=client_obj.id, ClientInitialBid=product_obj.Starting_Bid)
                auc_obj.save()
                auc_obj=Auction.objects.filter(ProductID=product_obj.id).order_by('-ClientInitialBid')
                return render(request, 'Auction/AucMain.html', {'Client':client_obj,'Product':product_obj,'RegUser':reg_user_obj, 'InAucUser':auc_obj})
            else:
                #filter() will always give you a QuerySet" - it's iterable
                #get() - return single object and it's not iterable
                auc_obj=Auction.objects.filter(ProductID=product_obj.id).order_by('-ClientInitialBid')
                if check.ClientUsername == reg_user_obj.User_Name:
                    return render(request, 'Auction/AucMain.html', {'Client':client_obj,'Product':product_obj,'RegUser':reg_user_obj, 'InAucUser':auc_obj})
        else:
            messages.warning(request, f'Invalid Credentials!.')
            return render(request,'Home/ErrorPage.html',{'Error':error})

