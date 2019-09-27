from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to ='image/slide_show/%Y/%m/%d', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
