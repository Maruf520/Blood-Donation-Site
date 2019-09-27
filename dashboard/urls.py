from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard1, name='dashboard'),
    path('upload_image/',views.image_upload, name='image_upload'),
    path('update/image', views.image_list, name = 'image_list'),
    path('delete/image/<int:id>/', views.delete, name= 'delete'),
]