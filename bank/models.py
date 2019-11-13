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
    ab_positive = models.FloatField(default=0)
    ab_negative = models.FloatField(default=0)
    a_positive = models.FloatField(default=0)
    a_negative = models.FloatField(default=0)
    b_positive = models.FloatField(default=0)
    b_negative = models.FloatField(default=0)
    o_positive = models.FloatField(default=0)
    o_negative = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Quantity(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
