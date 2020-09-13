from django.shortcuts import render
from .models import Blogpost


# Create your views here.


def index(request):
    myposts = Blogpost.objects.all()
    return render(request, 'forum/forum_index.html', {'myposts': myposts})


def blog_post(request, post_id):
    post = Blogpost.objects.filter(post_id=post_id)[0]
    return render(request, 'forum/blog_post.html', {'post': post})
