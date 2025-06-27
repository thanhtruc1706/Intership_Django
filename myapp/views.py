from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator

# Danh sách bài viết
def post_list(request):
    query = request.GET.get('q', '')
    post_list = Post.objects.all().order_by('-created_at')
    if query:
        post_list = post_list.filter(title__icontains=query) | post_list.filter(content__icontains=query)
    paginator = Paginator(post_list, 5)  # 5 bài viết mỗi trang
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'myapp/post_list.html', {'posts': posts, 'query': query})

# Chi tiết bài viết
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myapp/post_detail.html', {'post': post})

# Thêm bài viết
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_form.html', {'form': form})

# Sửa bài viết
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myapp/post_form.html', {'form': form})

# Xóa bài viết
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'myapp/post_confirm_delete.html', {'post': post})

# Đăng ký
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'myapp/register.html', {'form': form})
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('login')
        return render(request, 'myapp/register.html', {'form': form})

# Profile
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'myapp/profile.html', {'user_obj': request.user, 'posts': posts}) 