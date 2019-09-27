from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Comment
from accounts.models import Account
from post.forms import CommentPostForm


def blog_post_view(request):

    blog = Blog.objects.all()
    paginator = Paginator(blog, 1)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    context = {
        'blog': blog,
        'contacts': contacts
    }
    return render(request, 'home/blog_view/blog_page.html', context)


def individual_blog(request, id):

    if request.method == 'POST':
        post = get_object_or_404(Blog, id=id)
    
        form = CommentPostForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog = post
            new_comment.save()
            context = {
                'new_comment': new_comment
            }
            return render(request, 'home/blog_view/comment.html', context)

    else:
        comment = Comment.objects.filter(blog__id = id).all()
        form = CommentPostForm()
        post = Blog.objects.filter(id=id)

        context = {
            'post': post,
            'form': form,
            'comment': comment
        }
        return render(request, 'home/blog_view/comment.html', context)
