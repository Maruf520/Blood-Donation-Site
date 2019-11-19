from django.shortcuts import render, redirect,HttpResponse
from django.core.paginator import Paginator
from post.forms import BloodPostForm
from post.models import Blog 
from dashboard.models import Image,Commttee,Gallery
from notifications.signals import notify
from accounts.models import Account
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime,timedelta





def send_mail_to_user(to_mail_list, data):
    my_subject = "{} blood needed : Blood Bank".format(data.blood_group)
    my_message = """
    {} need {} bag {} blood at {} in {} , {}

    Message:
    {}


    Please Contact: 01710038888
    
    """.format(data.name, data.quantity, data.blood_group, data.location, data.time, data.date,data.description)
    send_mail(my_subject, my_message, 'blood.emergency0@gmail.com', to_mail_list,
            fail_silently=False)
def index(request):
    if request.method == 'POST':
        blogs = Blog.objects.all()
        image = Image.objects.all()
        form = BloodPostForm(request.POST,user=request.user)
        if form.is_valid():
            blog = form.save()
            all_account = Account.objects.filter(blood_group = blog.blood_group, last_date_of_donation__lte=datetime.now().date() - timedelta(days=100) )
            destination_emails = []
            destination_number = []
            for account in all_account:
                destination_emails.append(account.email)
                destination_number.append(account.phone)
                print(account.email)    
                print(account.phone)
            send_mail_to_user(destination_emails,blog)
                
            form = BloodPostForm()
            context = {'form': form,'blogs':blogs,'image':image}
            return render (request, 'home/blog_view/home_page_view.html', context)
        else:
            context = {'form': form}
            return render (request, 'home/homeSlideimage/slideimageHome.html', context) 
    else:
        blogs = Blog.objects.all().filter(managed=False)[:10]
        blog1 = Blog.objects.all().filter(managed=True).count()
        print(blog1)
        image_list = Image.objects.all()
        paginator = Paginator(blogs, 1)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        if request.user.is_authenticated:
            form = BloodPostForm(user=request.user)
        else:
            form = BloodPostForm()   
        
        context = {'form':form, 'blogs':blogs,'contacts': contacts,'image_list':image_list}
        return render (request, 'home/blog_view/home_page_view.html', context)

   
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
def ShowCommittee(request):

    committee = Commttee.objects.filter(session__icontains ='2016-2017')
    context = {
        'committee': committee
    }
    return render(request,'home/committee/committeehome.html',context)

def gallery(request):
    image =  Gallery.objects.all()

    context ={
        'image':image
    }

    return render(request, 'home/gallery/gallery.html',context)        

    
