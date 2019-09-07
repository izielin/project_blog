from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from .models import Post, Document, Comment, Cycle
from .forms import CommentForm, DocumentForm, CycleForm
from django.views import generic
from . import forms
from . import models
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.utils import timezone
from users.models import Profile
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

CATEGORY_CHOICES = Post.CATEGORY_CHOICES


def post_list(request):
    posts_list = Post.objects.filter(authorized=True).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(author__first_name__icontains=query) | Q(category__icontains=query) |
            Q(level__icontains=query)
        ).filter(authorized=True).distinct()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'most_popular': Post.objects.filter(authorized=True).order_by('-numbers_of_entries')[:4],
        'most_rated': Post.objects.filter(authorized=True).filter(ratings__isnull=False).order_by('-ratings__average')[
                      :4],
        'category': Post.objects.filter(authorized=True).values('category').annotate(Count('category')).order_by(
            'category'),
        'level': Post.objects.filter(authorized=True).values('level').annotate(Count('level')).order_by('level'),
        'newest': Post.objects.filter(authorized=True).filter(date_posted__gte=timezone.now()
                                                              .replace(hour=0, minute=0, second=0))
                      .order_by('-date_posted')[:1],
        'random': Post.objects.filter(authorized=True).order_by('?')[:3],
        'latest': Post.objects.filter(authorized=True).order_by('-date_posted')[:4],
    }
    return render(request, "blog/post_list.html", context)


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
            'category_abbr': form.cleaned_data['category'][:3],
            'author': self.request.user
        }

        recipients = []
        for prof in Profile.objects.filter(moderator=True):
            recipients.append(prof.user.email)

        subject = "Stworzono nowy kurs"
        message = "Otrzymujesz tę wiadomość, gdyż używkownik %s " \
                  "stworzył nowy kurs pod tytułem: '%s'\n" \
                  "Kurs oczekuje na autoryzajcę, proszę udaj się na stronę akceptacji. \n\n\n" \
                  "Szczegóły:\n" \
                  "Tytuł: %s,\n" \
                  "Autor: %s,\n" \
                  "Kategoria: %s,\n" \
                  "Data stowrzenia :%s\n" \
                  % (self.request.user, form.cleaned_data['title'], form.cleaned_data['title'], self.request.user,
                     form.cleaned_data['category'], datetime.now().date())

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

        instance = models.Post.objects.create(**kwargs)
        self.success_url = reverse('post-detail', kwargs={'pk': instance.id})
        return super(MDEditorFormView, self).form_valid(form)


class ShowView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShowView, self).get_context_data(**kwargs)
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
    template_name = 'blog/post_delete.html'
    success_message = 'Success: Post was deleted.'

    def get_success_url(self):
        return reverse('post-list')


def model_form_upload(request, pk):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.postId = pk
            form.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
    else:
        form = DocumentForm()
    return render(request, 'blog/file_form.html', {'form': form})


def download(request, pk):
    context = {
        'download_list': Document.objects.filter(postId=pk),
        'post': Post.objects.filter(id=pk)
    }

    return render(request, 'blog/file_list.html', context)


class DownloadDeleteView(BSModalDeleteView, LoginRequiredMixin):
    model = Document
    template_name = 'blog/file_delete.html'
    success_message = 'Success: File was deleted.'

    def get_success_url(self):
        id = self.object.postId
        return reverse('post-download', kwargs={'pk': id})


class CommentCreateView(BSModalCreateView, LoginRequiredMixin):
    template_name = 'blog/comment_form.html'
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
    template_name = 'blog/comment_delete.html'
    success_message = 'Success: Comment was deleted.'

    def get_success_url(self):
        id = self.object.post.id
        return reverse('post-detail', kwargs={'pk': id})


def posts_no_authorized(request):
    context = {
        'posts': Post.objects.filter(authorized=False).order_by('-date_posted')
    }
    return render(request, 'blog/no_authorized.html', context)

class CycleCreateView(BSModalCreateView, LoginRequiredMixin):
    template_name = 'blog/cycle_form.html'
    form_class = CycleForm

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        reverse_user = self.request.user
        return reverse('profile', kwargs={'username': reverse_user})


class CycleUpdateView(BSModalUpdateView):
    model = Cycle
    template_name = 'blog/cycle_update.html'
    form_class = CycleForm
    success_message = 'Success: Cycle was updated.'

    def get_success_url(self):
        reverse_user = self.request.user
        return reverse('profile', kwargs={'username': reverse_user})


class CycleDeleteView(BSModalDeleteView, LoginRequiredMixin):
    model = Cycle
    template_name = 'blog/cycle_delete.html'
    success_message = 'Success: Cycle was deleted.'

    def get_success_url(self):
        reverse_user = self.request.user
        return reverse('profile', kwargs={'username': reverse_user})