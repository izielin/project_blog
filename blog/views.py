from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
    DeleteView
)
from .models import Post, Document, Comment
from .forms import CommentForm, DocumentForm
from django.views import generic
from . import forms
from . import models
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


def about(request):
    posts_list = Post.objects.filter(authorized=True).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(author__first_name__icontains=query) | Q(category__icontains=query) | Q(level__icontains=query)
        ).filter(authorized=True).distinct()
    paginator = Paginator(posts_list, 6)  # 6 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'most_popular': Post.objects.filter(authorized=True).order_by('-numbers_of_entries')[:3],
        'most_rated': Post.objects.filter(authorized=True).filter(ratings__isnull=False).order_by('-ratings__average')[:3],
        'category': Post.objects.filter(authorized=True).values('category').annotate(Count('category')).order_by('category'),
        'level': Post.objects.filter(authorized=True).values('level').annotate(Count('level')).order_by('level'),
    }
    return render(request, "blog/about.html", context)


def home(request):
    context = {
        'posts': Post.objects.filter(authorized=True).order_by('-date_posted')[:4]
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
            'author': self.request.user
        }
        instance = models.Post.objects.create(**kwargs)
        self.success_url = reverse('post-detail', kwargs={'pk': instance.id})
        return super(MDEditorFormView, self).form_valid(form)


class ShowView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.numbers_of_entries = self.object.numbers_of_entries + 1
        self.object.save()
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    def form_valid(self, form):
        form.instance.status = 'Approved'
        form.instance.author = form.instance.author
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.moderator == True:
            self.fields = ['title', 'synopsis', 'category', 'level', 'authorized', 'content', 'status']
        else:
            self.fields = ['title', 'synopsis', 'category', 'content']
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.profile.moderator == True:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/about'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def model_form_upload(request, pk):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.postId = pk
            form.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
    else:
        form = DocumentForm()
    return render(request, 'blog/upload.html', {'form': form})


def download(request, pk):
    context = {
        'download_list': Document.objects.filter(postId=pk),
        'post': Post.objects.filter(id=pk)
    }

    return render(request, 'blog/download.html', context)


class DownloadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document

    def get_success_url(self):
        id = self.object.postId
        return reverse('post-download', kwargs={'pk': id})

    def test_func(self):
        return True


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


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        id = self.object.post.id
        return reverse('post-detail', kwargs={'pk': id})

    def test_func(self):
        return True


def posts_no_authorized(request):
    context = {
        'posts': Post.objects.filter(authorized=False).order_by('-date_posted')
    }
    return render(request, 'blog/no_authorized.html', context)

