from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.conf import settings

from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'catatan/post_list.html', {'list_post': posts})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'catatan/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'catatan/post_edit.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'catatan/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    draftposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'catatan/post_draft_list.html', {'draftposts': draftposts})


@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('post_detail', post_id=post_id)


@login_required
def post_remove(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post_list')


@login_required
def logout_view(request):
    logout(request)
    return redirect('post_list')


# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             return redirect('post_list')
#         else:
#             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#     else:
#         return redirect('post_list')

def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'catatan/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('post_detail', post_id=comment.post.pk)


@login_required
def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, post_id=comment_id)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', post_id=post_pk)
