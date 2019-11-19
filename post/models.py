from accounts.models import Account 
from django.db import models
from django.utils import timezone 
from django.core.validators import MaxValueValidator, MinValueValidator
from notifications.signals import notify
from accounts.models import Account
from django.db.models.signals import post_save

_BLOOD_GROUPS = (
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
)

class Blog(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE, blank=True, null=True )
    name = models.CharField(max_length=80)
    blood_group = models.CharField(max_length = 3, choices=_BLOOD_GROUPS)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveSmallIntegerField(default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
     )
    location = models.TextField(blank = False, null = False)
    description = models.TextField(blank=True, null = True)
    phone =  models.CharField(max_length=15,blank=False,null=False)
    managed = models.BooleanField(default=False)
    date = models.DateField( blank=False)
    time = models.TimeField( blank = False)


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance.user, recipient = instance.user, description = Comment.text,verb='You have a fucking notification for new Comment')

post_save.connect(my_handler, sender=Comment) 

# Create your models here.
