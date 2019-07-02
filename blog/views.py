from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    UpdateView,
    DeleteView
)
from .models import Post, FileUploadUrl
from .filters import PostFilter
from django.core.files.storage import FileSystemStorage
from .forms import CommentForm
from django.views import generic
from . import forms
from . import models

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


def about(request):
    post_list = Post.objects.all().order_by('-date_posted')
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'blog/about.html', {'filter': post_filter})


def home(request):
    context = {
        'posts': Post.objects.filter(authorized=True).order_by('-id')[:4]
    }
    return render(request, 'blog/home.html', context)


class MDEditorFormView(generic.FormView):
    form_class = forms.MDEditorForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        kwargs = {
            'title': form.cleaned_data['title'],
            'synopsis': form.cleaned_data['synopsis'],
            'content': form.cleaned_data['content'],
            'category': form.cleaned_data['category'],
            'level': form.cleaned_data['level'],
            'author': self.request.user
        }
        instance = models.Post.objects.create(**kwargs)
        self.success_url = reverse('post-detail', kwargs={'pk': instance.id})
        return super(MDEditorFormView, self).form_valid(form)


class ShowView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    # def pattern(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         fields = ['title', 'synopsis', 'category', 'level', 'content']
    #     else:
    #         fields = ['title', 'synopsis', 'category', 'level', 'authorized', 'content', 'status']
    #     return fields
    # fields = pattern()
    fields = ['title', 'synopsis', 'category', 'level', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class MPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'synopsis', 'category', 'level', 'status', 'authorized', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.moderator == True:
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

    post = Post.objects.filter(id=pk)
    return render(request, 'blog/download.html', context, post)


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


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/addComment.html', {'form': form})


def posts_no_authorized(request):
    context = {
        'posts': Post.objects.filter(authorized=False).order_by('-date_posted')
    }
    return render(request, 'blog/no_authorized.html', context)