from django.contrib import admin

from . models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','blood_group','phone','address','is_staff','last_date_of_donation','is_admin','is_active','is_staff','is_superuser')
    list_editable = ('blood_group','phone','address','is_staff','last_date_of_donation','is_admin','is_active','is_staff','is_superuser')
admin.site.register(Account,AccountAdmin)    