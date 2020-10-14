# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djmoney.models.fields import MoneyField
import datetime
from django.utils.translation import gettext as _

# Create your models here.

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    sessionId = models.CharField(max_length=250,blank=True)  
    created_date = models.DateTimeField(auto_now_add=True)
    booking_ref = models.CharField(max_length=250,blank=True)
    user_id = models.IntegerField()
    agent_ref = models.CharField(max_length=250,blank=True)
    notes = models.CharField(max_length=500,blank=True)
    status = models.IntegerField()
    currency_id = models.IntegerField()
    settlementprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    netprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    grossprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    commissionprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    bookingfeeprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')


class CartProducts(models.Model):
    id = models.AutoField(primary_key=True)
    cart =  models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
               
    )
    product_name = models.CharField(max_length=250,blank=True)
    fare = models.CharField(max_length=250,blank=True)
    validity =models.CharField(max_length=250,blank=True)
    service = models.CharField(max_length=250,blank=True)
    Rule = models.CharField(max_length=2000,blank=True)
    product_id = models.IntegerField()    
    start_date = models.DateField()    
    passengers_num = models.IntegerField()
    status = models.IntegerField()
    settlementprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    netprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    grossprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    commissionprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    
class CartProductDetails(models.Model):
    id = models.AutoField(primary_key=True)
    cart_product =  models.ForeignKey(
        'CartProducts',
        on_delete=models.CASCADE,        
    )
    from_station = models.CharField(max_length=250,blank=True)
    to_station = models.CharField(max_length=250,blank=True) 
    from_code = models.CharField(max_length=20,blank=True)
    to_code = models.CharField(max_length=20,blank=True) 
    departure_date = models.DateTimeField(auto_now_add=True)
    arrival_date = models.DateTimeField(auto_now_add=True)
    train = models.CharField(max_length=20,blank=True)
    train_category = models.CharField(max_length=50,blank=True)
    netprice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    passengers_num = models.IntegerField()
    
    
class CartProductPassengers(models.Model):
    id = models.AutoField(primary_key=True)
    cart_product =  models.ForeignKey(
        'CartProducts',
        on_delete=models.CASCADE,        
    )
    title =  models.CharField(max_length=50,blank=True)
    first_name = models.CharField(max_length=250,blank=True)
    last_name = models.CharField(max_length=250,blank=True)    
    age = models.IntegerField()
    dob = models.DateField(_("Date"))    
    nationality = models.CharField(max_length=20,blank=True)
    passport = models.CharField(max_length=50,blank=True)
