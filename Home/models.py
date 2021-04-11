from django.db import models
from django.conf import settings
from django.conf.urls.static import static

# Create your models here.
class Client(models.Model):
    #u_id=models.AutoField(primary_key=True)
    First_name=models.CharField(max_length=20)
    Last_name=models.CharField(max_length=20)
    Uname=models.CharField(max_length=30,unique=True)
    Profile_pic = models.ImageField(upload_to= 'user_img', default='')
    DOB=models.DateField()
    Choices=[('Male','Male'),('Female','Female'),('Others','Others')]
    Gender=models.CharField(max_length=6,choices=Choices)
    Aadhar=models.CharField(max_length=12)
    Email=models.CharField(max_length=50)
    Contact=models.CharField(max_length=13)
    Address=models.CharField(max_length=255)
    Work_status=models.CharField(max_length=255)
    Work_desc=models.CharField(max_length=255)
    password=models.CharField(max_length=15)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.Uname

class Product(models.Model):
    Product_id = models.AutoField
    Prod_Owner_info = models.ForeignKey(Client, null=True,on_delete=models.CASCADE)
    Product_owner = models.CharField(max_length=40)
    Product_name = models.CharField(max_length=100)
    Product_bought_date = models.DateField()
    Starting_Bid = models.IntegerField()
    Auction_pref_date = models.DateField()
    Auction_pref_time = models.TimeField()
    Product_desc = models.CharField(max_length=255)
    Product_img = models.ImageField(upload_to= 'auction_prod')
    Auction_Passcode = models.CharField(max_length=5)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.Product_name

class Cont_us(models.Model):
    Full_name=models.CharField(max_length=30)
    Last_name=models.CharField(max_length=30)
    email_addr=models.CharField(max_length=100)
    ph_no=models.CharField(max_length=12)
    Content=models.TextField()
    timeStamp1=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from: ' + self.Full_name + ' ' + self.Last_name

# Users who Pre-register for an auction.
class Registered_Users(models.Model):
    User_Name = models.CharField(max_length=30)
    User_Email=models.CharField(max_length=50)
    Product_Name = models.CharField(max_length=100)
    Product_Owner = models.CharField(max_length=40)
    Product_ID = models.IntegerField()
    Auction_date = models.DateField()
    Auction_time = models.TimeField()
    Initial_Bid_Amt = models.IntegerField()
    PassCode = models.CharField(max_length=5)
    TimeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Pre-Registered User: ' + self.User_Name