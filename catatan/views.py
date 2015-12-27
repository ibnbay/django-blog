from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'catatan/post_list.html', {'list_post': posts})

# def post_detail(request, post_id):
#     posts = Post.objects.get(pk=post_id)
#     return render(request, 'catatan/post_detail.html', {'list_post': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'catatan/post_detail.html', {'post': post})
