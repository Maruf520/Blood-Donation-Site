from django.contrib import admin
from .models import Bank, Blood
# Register your models here.


class BankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Bank, BankAdmin)


class BloodAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    # list_display = ['group', 'slug', 'price', 'stock',
    #                 'available', 'created_at', 'updated_at']
    list_display = ['id', 'group', 'price', 'stock',
                    'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    # prepopulated_fields = {'slug': ('bank', 'group',)}

    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     if db_field.name == "group":
    #         A_POSITIVE = 'A_positive'
    #         A_NEGATIVE = 'A_negative'
    #         B_POSITIVE = 'B_positive'
    #         B_NEGATIVE = 'B_negative'
    #         AB_POSITIVE = 'AB_positive'
    #         AB_NEGATIVE = 'AB_negative'
    #         O_POSITIVE = 'O_positive'
    #         O_NEGATIVE = 'O_negative'
    #         kwargs['choices'] = (
    #             (A_POSITIVE, 'A+'),
    #             (A_NEGATIVE, 'A-'),
    #             (B_POSITIVE, 'B+'),
    #             (B_NEGATIVE, 'B-'),
    #             (AB_POSITIVE, 'AB+'),
    #             (AB_NEGATIVE, 'AB-'),
    #             (O_POSITIVE, 'O+'),
    #             (O_NEGATIVE, 'O-'),
    #         )
    #         if request.user.is_superuser:
    #             kwargs['choices'] += (('ready', 'Ready for deployment'),)
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(Blood, BloodAdmin)
