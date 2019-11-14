from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to ='image/slide_show/%Y/%m/%d', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Commttee(models.Model):
    name = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    session = models.CharField(max_length=30)
    image = models.ImageField(upload_to ='image/commttee/%Y/%m/%d',blank=False)

class Gallery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image =  image = models.ImageField(upload_to ='image/gallery/%Y/%m/%d', blank=False)
