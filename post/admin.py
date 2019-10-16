from django.contrib import admin

# Register your models here.
from . models import Blog,Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','name','blood_group','quantity','location','description','phone', 'date','time')
    list_editable = ('description','name')

admin.site.register(Blog,BlogAdmin)