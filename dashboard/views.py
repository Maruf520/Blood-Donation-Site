from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse 
from dashboard.forms import SlidImageForm
from dashboard.models import Image
from post.models import Blog, Comment
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from .filters import UserFilter
from datetime import datetime
from dashboard.models import Commttee,Gallery
from dashboard.forms import CommitteeForm,DropDownForm,CommitteeForm,GalleryImageForm,ReportForm,AccountUpdateForm
from django.views import generic
from django.urls import reverse
from datetime import datetime, timedelta

@login_required(login_url='login')
def dashboard1(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    total_user = Account.objects.all().count()
    total_post = Blog.objects.all().count()
    context = {
        'total_user': total_user,
        'total_post': total_post
    }    
    # return render(request,'Dashboard/base.html')
    return render(request, 'dashboard/base.html', context)

@login_required(login_url='login')
def image_upload(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        form = SlidImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            # print(image)
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
@login_required(login_url='login')
def image_list(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'GET':
        photo_list = Image.objects.all()

        context = {
            'photo_list' : photo_list
        }
    return render(request,'dashboard/upload_image/image_list.html', context)
@login_required(login_url='login')
def delete_image(request, id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        image_list = Image.objects.get(id = id)
        image_list.delete()
        return redirect('image_list')
@login_required(login_url='login')
def manage_post(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    post = Blog.objects.all()
    comment  = Comment.objects.all()

    context = {
        'post':post,
        'comments' : comment
        
    }
    return render(request, 'dashboard/manage_post/manage_post.html', context)
@login_required(login_url='login')    
def delete_post(request,id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        post = Blog.objects.get(id = id)
        post.delete()
        return redirect('manage_post')
@login_required(login_url='login')
def individual_post(request, id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'GET':
        post_item = Blog.objects.filter(id = id)
        comments = Comment.objects.filter(blog__id = id).all()

        context ={
            'post_item' : post_item,
            'comments' : comments
        }
    return render(request, 'dashboard/manage_post/individual_post.html', context)

@login_required(login_url='login')
def delete_comment(request, id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    comment = Comment.objects.filter(id = id).first()
    comment.delete()

    # To return to the pervious page use this code
    # return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def user_list(request):

    if not request.user.is_staff: 
        return render(request, 'home/ErrorPage/permission.html') 
    user = Account.objects.all()

    context ={
        'users':user
    }     
    return render(request, 'dashboard/users/users.html', context)  
@login_required(login_url = 'login')
def single_user (request, id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    single_user = Account.objects.get(id = id)
    
    a = datetime.now().date()-single_user.last_date_of_donation
    b = a.days
    print(b)
 
    context = {
        'single_user': single_user,
        'b':b,
        
    }
    return render (request, 'dashboard/users/single_user.html', context)
@login_required(login_url = 'login')    
def delete_single_user(request, id):
    
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    delete_user = Account.objects.get(id = id)
    print(delete_user)
    delete_user.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url = 'login')
def search(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    user_list = Account.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'dashboard/users/search.html', {'filter': user_filter})

@login_required(login_url = 'login')
def committee_form(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        form = CommitteeForm(request.POST,request.FILES)
        if form.is_valid():
            committee = form.save()
            return redirect("dashboard")
    else:
        form = CommitteeForm()

        context = {
            'form': form
        }    
    return render(request, 'dashboard/committee/committee_form.html',context)    
@login_required(login_url = 'login')
def committee(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')

    session_list = DropDownForm()

    if request.GET.get('session'):
        selected_session = request.GET.get('session')

        query_results = Commttee.objects.filter(session= selected_session )
    else:
        query_results = Commttee.objects.filter(session__icontains ='2016-2017')

    context = {
        'query_results':query_results,
        'session_list':session_list,
    }    
    return render(request, 'dashboard/committee/committee_list.html',context)
        
@login_required(login_url = 'login')
def Committee_member(request, id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'GET':
        member = Commttee.objects.get( id = id )
        print(member)
    context = {
        'member':member,
    }    

    return render(request,'dashboard/committee/committee_member.html',context)
          


class CommtteeUpdateView(generic.UpdateView):
    model = Commttee
    fields = ['name','designation','session','image']
    template_name_suffix = "_update_form"

    def form_valid(self,form):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return super(CommtteeUpdateView, self).form_valid(form)
        else:
            HttpResponse('Balchal')    
    def get_success_url(self):
        return reverse('view_committee')
@login_required(login_url = 'login')
def GalleryImage(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        form = GalleryImageForm (request.POST,request.FILES)
        if form.is_valid():
            form.save() 
            return redirect("gelleryImage")
    else:
        form =   GalleryImageForm()

    context = {
        'form':form
    }              
    return render(request,'dashboard/gallery/galleryimage.html',context)  
@login_required(login_url = 'login')
def GalleryImageView(request):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    image =  Gallery.objects.all()
    print(image)
    context = {
        'image':image
    }
    return render (request,'dashboard/gallery/galleryimageview.html',context)
@login_required(login_url = 'login')
def GalleryImageManage(request,id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'POST':
        image_del = Gallery.objects.get(id=id)
        image_del.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url = 'login')
def updateAccount(request, id ):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    user = Account.objects.get(id=id)
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST,request.FILES,user=user)
        if form.is_valid():
            form1 = form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        form = AccountUpdateForm(user=user)
    context = {
        'form':form
    }
    return render(request, 'dashboard/users/userupdate.html', context)
@login_required(login_url = 'login')
def managePost(request,id):
    if not request.user.is_staff:
        return render(request, 'home/ErrorPage/permission.html')
    if request.method == 'GET':
        post = Blog.objects.get(id=id)
        post.managed = True
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

def report(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReportForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/')) 
        else:
            return HttpResponse(form.errors.__str__())







