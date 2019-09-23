from django.shortcuts import render, redirect,HttpResponse
from django.core.paginator import Paginator
from post.forms import BloodPostForm
from post.models import Blog 

# Create your views here.

def index(request):
    
    if request.method == 'POST':
        blogs = Blog.objects.all()
        form = BloodPostForm(request.POST)
        if form.is_valid():
            blog = form.save()
            print(blog)
            form = BloodPostForm()
            context = {'form': form,'blogs':blogs}
            return render (request, 'home/blog_view/blog_view.html', context)
        else:
            context = {'form': form}
            return render (request, 'home/base.html', context)

        
    else:
        blogs = Blog.objects.all().order_by('-id')
        paginator = Paginator(blogs, 3)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        if request.user.is_authenticated:
            form = BloodPostForm(user=request.user)
        else:
            form = BloodPostForm()   
        
        context = {'form':form, 'blogs':blogs,'contacts': contacts}
        return render (request, 'home/blog_view/blog_view.html', context)

def blog_post_view(request):

        blog = Blog.objects.all() 

        context ={
            'blog': blog
        }   
        return render(request, 'home/blog_view/blog_page.html', context)


     

    # context = {
    #     'form': form, 
    #     'view_post': view_post
    # }
    # return render (request, 'home/base.html', context)

# def view_blog(request):
#     view_list = Blog.objects.all()

        
#     return render(request, 'home/base.html',{'context':view_list})
