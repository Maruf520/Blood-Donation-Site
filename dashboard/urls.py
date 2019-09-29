from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard1, name='dashboard'),
    path('upload_image/',views.image_upload, name='image_upload'),
    path('update/image', views.image_list, name = 'image_list'),
    path('delete/image/<int:id>/', views.delete_image, name= 'delete'),
    path('manage_post', views.manage_post, name= 'manage_post'),
    path('manage_post/<int:id>', views.delete_post, name='delete_post'),
    path('manage/individual/<int:id>', views.individual_post, name = 'individual_post'),
     path('manage/individual/<int:id>', views.individual_post, name = 'delete_individual_comment'),


]