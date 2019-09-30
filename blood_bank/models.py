from django.db import models

class Bank_details(models.Model):
    bank_name = models.CharField(max_length=300,blank=False)
    bank_location =  models.CharField(max_length=300,blank=False)
    bank_logo = models.ImageField(upload_to ='image/bank_logo/%Y/%m/%d', blank=False)
    bank_contact =models.CharField(max_length=20,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Blood_quantity (models.Model):
    bank = models.ForeignKey(Bank_details, on_delete = models.CASCADE )
    ab_p = models.FloatField(default=0.0)
    ab_n = models.FloatField(default=0.0)
    a_p = models.FloatField(default=0.0)
    a_n = models.FloatField(default=0.0)
    b_p = models.FloatField(default=0.0)
    b_n = models.FloatField(default=0.0)
    o_p = models.FloatField(default=0.0)
    o_n = models.FloatField(default=0.0)

       