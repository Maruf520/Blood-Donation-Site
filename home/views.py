from django.shortcuts import render, redirect,HttpResponse
from django.core.paginator import Paginator
from post.forms import BloodPostForm
from post.models import Blog 
from dashboard.models import Image

# Create your views here.

def index(request):
    
    if request.method == 'POST':
        blogs = Blog.objects.all()
        image = Image.objects.all()
        form = BloodPostForm(request.POST)
        if form.is_valid():
            blog = form.save()
            print(blog)
            form = BloodPostForm()
            context = {'form': form,'blogs':blogs,'image':image}
            return render (request, 'home/blog_view/blog_view.html', context)
        else:
            context = {'form': form}
            return render (request, 'home/base.html', context)

        
    else:
        blogs = Blog.objects.all().order_by('-id')
        image_list = Image.objects.all()
        paginator = Paginator(blogs, 1)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        if request.user.is_authenticated:
            form = BloodPostForm(user=request.user)
        else:
            form = BloodPostForm()   
        
        context = {'form':form, 'blogs':blogs,'contacts': contacts,'image_list':image_list}
        return render (request, 'home/blog_view/blog_view.html', context)

def blog_post_view(request, id):

        blog = Blog.objects.all()
        paginator = Paginator(blog, 1)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)

        context ={
            'blog': blog,
            'contacts': contacts
        }   
        return render(request, 'home/blog_view/blog_page.html', context)

    
