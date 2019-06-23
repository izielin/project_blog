from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, FileUploadUrl
from .filters import PostFilter
from django.core.files.storage import FileSystemStorage


def about(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'blog/about.html', {'filter': post_filter})


def home(request):
    context = {
        'posts': Post.objects.all().order_by('-id')[:3]
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/about.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'level', 'synopsis', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'level', 'synopsis', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def download(request, pk):
    context = {
        'download_list': FileUploadUrl.objects.filter(postId=pk)
    }
    return render(request, 'blog/download.html', context)


class DownloadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FileUploadUrl
    success_url = '/'

    def test_func(self):
        return True


def simple_upload(request, pk):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        url = FileUploadUrl(fileName=myfile, url=uploaded_file_url, postId=pk)
        url.save()
        messages.success(request, f'Success! You can add another file!')
        return render(request, 'blog/simple_upload.html')
    return render(request, 'blog/simple_upload.html')
