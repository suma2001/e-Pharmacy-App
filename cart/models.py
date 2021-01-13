from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from user.models import Shop

class Document(models.Model):
    # description = models.CharField(max_length=255, blank=True)
    docfile = models.FileField(upload_to='documents/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(blank=True,null=True)
    description = models.CharField(max_length=300)
    in_cart = models.BooleanField(default=False)
    image = models.CharField(blank=True, null=True, max_length=400)
    shop_having = models.ManyToManyField("user.Shop")

    def __str__(self):
        return self.name

class Cart(models.Model):
    #current_user =  models.ForeignKey(User, on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    itemtotal=models.FloatField(blank=True,null=True)
    #
    # def __str__(self):
    #     return str(self.current_user.username)

    def get_total_item_price(self):
        return self.quantity*self.item.price


