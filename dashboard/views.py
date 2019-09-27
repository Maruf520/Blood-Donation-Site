from django.shortcuts import render,redirect
from django.http import HttpResponse 
from dashboard.forms import SlidImageForm
from dashboard.models import Image


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

def delete(request, id):
    if request.method == 'POST':
        image_list = Image.objects.get(id = id)
        image_list.delete()
        return redirect('image_list')

