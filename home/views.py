from django.shortcuts import render, redirect,HttpResponse
from django.core.paginator import Paginator
from post.forms import BloodPostForm
from post.models import Blog 
from dashboard.models import Image
from notifications.signals import notify
from accounts.models import Account
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime


def send_mail_to_user(to_mail):
    send_mail('about testing', 'hi rafiul, ', 'md.maruf5201@gmail.com', [to_mail],
            fail_silently=False)



# Create your views here.
def index(request):
    if request.method == 'POST':
        blogs = Blog.objects.all()
        image = Image.objects.all()
        form = BloodPostForm(request.POST)
        if form.is_valid():
            blog = form.save()
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(datetime.now().date()), date_format)
            b = datetime.strptime(str(Account.last_date_of_donation),date_format)
            c = a-b
            # print(c.days)
            d = c.days
            all_account = Account.objects.filter(last_date_of_donation.days > 40 ).filter(blood_group = blog.blood_group)
            for account in all_account:
                send_mail_to_user(account.email)
                print(account.email)
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

    
