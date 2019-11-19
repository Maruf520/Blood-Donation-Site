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
    path('manage/individual/comment/<int:id>', views.delete_comment, name = 'delete_individual_comment'),
    path('users/',views.user_list, name='userlist'),
    path('users/<int:id>/',views.single_user, name='signle_user'),
    path('user/delete/<int:id>/', views.delete_single_user, name='delete_single_user'),
    path('search/', views.search, name='search'),
    path('committee/add_committee/', views.committee_form, name='committee'),
    path('committee/list', views.committee,name='view_committee'),
    path('committee/list/<int:id>/', views.Committee_member,name='committee_member'),
    path('committee/list/edit/<int:pk>/', views.CommtteeUpdateView.as_view() ,name='editcommittee'),
    path('gallery/image/upload',views.GalleryImage, name='gelleryImage'),
    path('gallery/delete/image/<int:id>/',views.GalleryImageManage, name='deleteImage'),
    path('gallery/image/view/',views.GalleryImageView, name='galleryimageview'),
    path('users/<int:id>/update/', views.updateAccount,name='userupdate'),
    path('post/<int:id>/managed/', views.managePost,name='postmanaged'),




]