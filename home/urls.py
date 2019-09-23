from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.blog_post_view, name='blood_blog'),
    path('', views.index, name='index')
    
]