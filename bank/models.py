from django.db import models
from accounts.models import Account
from django.utils import timezone
import datetime


class Bank(models.Model):
    name = models.CharField(max_length=300, blank=False)
    location = models.CharField(max_length=300, blank=False)
    logo = models.ImageField(
        upload_to='image/bank_logo/%Y/%m/%d', blank=False)
    contact = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())


class Quantity (models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    ab_p = models.FloatField(default=0.0)
    ab_n = models.FloatField(default=0.0)
    a_p = models.FloatField(default=0.0)
    a_n = models.FloatField(default=0.0)
    b_p = models.FloatField(default=0.0)
    b_n = models.FloatField(default=0.0)
    o_p = models.FloatField(default=0.0)
    o_n = models.FloatField(default=0.0)
