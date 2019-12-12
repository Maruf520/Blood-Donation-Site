from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .validators import valid_group
from django.shortcuts import redirect
from accounts.models import Account


class Bank(models.Model):
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    location = models.CharField(max_length=300, blank=False)
    logo = models.ImageField(
        upload_to='image/bank_logo/%Y/%m/%d', blank=False)
    contact = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'bank'
        verbose_name_plural = 'banks'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blood:blood_list_by_bank', kwargs={'bank_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bank, self).save(*args, **kwargs)


class Blood(models.Model):
    A_POSITIVE = 'A_positive'
    A_NEGATIVE = 'A_negative'
    B_POSITIVE = 'B_positive'
    B_NEGATIVE = 'B_negative'
    AB_POSITIVE = 'AB_positive'
    AB_NEGATIVE = 'AB_negative'
    O_POSITIVE = 'O_positive'
    O_NEGATIVE = 'O_negative'
    choices = [
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
    ]
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    group = models.CharField(
        choices=choices, max_length=11, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return redirect('blood:bank-list')

    class Meta:
        ordering = ('group',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return "%s %s" % (self.id, self.stock)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.bank)+"-"+self.group)
        super(Blood, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blood:product_detail', kwargs={'id': self.id, 'slug': self.slug})
    # def group_validators(self):
    #     if self.group and self.bank.blood_set.filter(group=self.group).exists():
    #         raise ValidationError(
    #             _('is not an even number'))
