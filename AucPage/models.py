from django.db import models
from Home.models import Product

# Create your models here.
class Auction(models.Model):
    OwnerName = models.CharField(max_length=30)
    #OwnerID = models.IntegerField()
    #ProductName = models.CharField(max_length=100)
    ProductID = models.IntegerField()
    ClientUsername = models.CharField(max_length=30)
    ClientID = models.IntegerField()
    ClientInitialBid = models.IntegerField()
    Winner = models.CharField(max_length=3, default='No')
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
    


    def __str__(self):
        return self.ClientUsername + ' in Auction of '
        #return self.ClientUsername + ' in Auction of ' + self.Product.ProductID