from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Blog, Comment
from accounts.models import Account
from post.forms import CommentPostForm



def blog_post_view(request):

    blog = Blog.objects.filter(managed = False).order_by('-created')
    paginator = Paginator(blog, 1)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    comments = Comment.objects.all()
    print(blog)
    form = CommentPostForm()
    context = {
        'blog': blog,
        'comments' : comments,
        'contacts': contacts,
        'form' : form
    }
    return render(request, 'home/blog_view/blog_page.html', context)


def individual_blog(request, id):

    if request.method == 'POST':
        post = get_object_or_404(Blog, id=id)
    
        form = CommentPostForm(request.POST, user=request.user, post=post)
        if form.is_valid():
            new_comment = form.save()
            return redirect("blood_blog")

    return HttpResponse("Something went wrong", status=400)
def managedPost(request):
    managepost = Blog.objects.filter(managed = True)
    print(managepost)
    context = {
        'managedpost': managepost
    }
    return render (request,'home/blog_view/managedpost.html',context)
        
