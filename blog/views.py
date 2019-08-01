from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
    DeleteView
)
from .models import Post, Document, Comment
# from .forms import CommentForm, DocumentForm, QueueForm
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
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)


def about(request):
    posts_list = Post.objects.filter(authorized=True).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(author__first_name__icontains=query) | Q(category__icontains=query) |
            Q(level__icontains=query)
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
        'most_rated': Post.objects.filter(authorized=True).filter(ratings__isnull=False).order_by('-ratings__average')[
                      :3],
        'category': Post.objects.filter(authorized=True).values('category').annotate(Count('category')).order_by(
            'category'),
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


class PostDeleteView(BSModalDeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/postDelete.html'
    success_message = 'Success'
    success_url = '/about'


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


class DownloadDeleteView(BSModalDeleteView, LoginRequiredMixin):
    model = Document
    template_name = 'blog/fileDelete.html'
    success_message = 'Success: File was deleted.'

    def get_success_url(self):
        id = self.object.postId
        return reverse('post-download', kwargs={'pk': id})


class CommentCreateView(BSModalCreateView, LoginRequiredMixin):
    template_name = 'blog/addComment.html'
    form_class = CommentForm

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        id = self.object.post.id
        return reverse('post-detail', kwargs={'pk': id})


class CommentDeleteView(BSModalDeleteView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/deleteComment.html'
    success_message = 'Success: Comment was deleted.'

    def get_success_url(self):
        id = self.object.post.id
        return reverse('post-detail', kwargs={'pk': id})

# def add_queue(request):
#     if request.method == "POST":
#         form = QueueForm(request.POST)
#         form.instance.author = request.user
#         if form.is_valid():
#             queue = form.save(commit=False)
#             queue.save()
#             return redirect('home')
#     else:
#         form = CommentForm()
#     return render(request, 'blog/addQueue.html', {'form': form})


def posts_no_authorized(request):
    context = {
        'posts': Post.objects.filter(authorized=False).order_by('-date_posted')
    }
    return render(request, 'blog/no_authorized.html', context)
