from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse 
from dashboard.forms import SlidImageForm
from dashboard.models import Image
from post.models import Blog, Comment


def dashboard1(request):

    # return render(request,'Dashboard/base.html')

    return render(request, 'dashboard/base.html')

def image_upload(request):
    if request.method == 'POST':
        form = SlidImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            print(image)
            return redirect('image_upload')
        print(form.errors)
        return HttpResponse("failed")
            
    else:
        form = SlidImageForm()  
        context = {
            'form':form
        }
        return render (request, 'dashboard/upload_image/image_upload.html',context)       

    return render (request, 'dashboard/upload_image/image_upload.html')    

def image_list(request):
    if request.method == 'GET':
        photo_list = Image.objects.all()

        context = {
            'photo_list' : photo_list
        }
    return render(request,'dashboard/upload_image/image_list.html', context)

def delete_image(request, id):
    if request.method == 'POST':
        image_list = Image.objects.get(id = id)
        image_list.delete()
        return redirect('image_list')

def manage_post(request):
    post = Blog.objects.all()
    comment  = Comment.objects.all()

    context = {
        'post':post,
        'comments' : comment
        
    }
    return render(request, 'dashboard/manage_post/manage_post.html', context)

def delete_post(request,id):
    if request.method == 'POST':
        post = Blog.objects.get(id = id)
        post.delete()
        return redirect('manage_post')

def individual_post(request, id):
    if request.method == 'GET':
        post_item = Blog.objects.filter(id = id)
        comments = Comment.objects.filter(blog__id = id).all()

        context ={
            'post_item' : post_item,
            'comments' : comments
        }
    return render(request, 'dashboard/manage_post/individual_post.html', context)


def delete_comment(request, id):
    comment = Comment.objects.filter(id = id).first()
    comment.delete()

    # To return to the pervious page use this code
    # return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))

        
