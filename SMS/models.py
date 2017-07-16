from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Clients(models.Model):

    client_id = models.AutoField(primary_key=True)
    client_coupon = models.CharField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=20, null=True)
    logged_in = models.BooleanField(default=False)

    def __str__(self):
        return self.client_coupon

class Admin(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)

class Templates(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=1000)
    sender_title = models.CharField(max_length=1000)
    template_body = models.TextField()

    def __str__(self):
        return self.company_name



class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(Templates,null=True,blank=True)
    user_id = models.ForeignKey(Clients,null=True,blank=True)
    message_time = models.CharField(max_length=1000, null=True,blank=True)
    date = models.CharField(max_length=1000, null=True,blank=True)
    time = models.CharField(max_length=1000, null=True,blank=True)
    vendor = models.CharField(max_length=1000, null=True,blank=True)
    name = models.CharField(max_length=1000, null=True,blank=True)
    orderId = models.CharField(max_length=1000, null=True,blank=True)
    sender = models.CharField(max_length=1000, null=True,blank=True)
    amount = models.CharField(max_length=1000, null=True,blank=True)
    scrapedPrice = models.CharField(max_length=10, null=True, blank=True)
    scrapedName = models.CharField(max_length=1000, null=True,blank=True)
    message = models.TextField()

    def __unicode__(self):
        return self.name

    @property
    def company_name(self):
        return self.template.company_name

    @property
    def client_coupon(self):
        return self.user_id.client_coupon
