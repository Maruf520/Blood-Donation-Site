from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog_post_view, name='blood_blog'),
    path('blog/comment/<int:id>', views.individual_blog, name='single_blog'),


]
