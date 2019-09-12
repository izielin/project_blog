from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post, Cycle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')

            def get_success_url(self, request):
                reverse_user = request.user
                return reverse('profile', kwargs={'username': reverse_user})

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    posts_list = Post.objects.filter(author=user)
    paginator = Paginator(posts_list, 8)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # for title, id in Cycle.objects.filter(author=request.user).values_list('title', 'posts'):
    #     print(title, id)

    cycles = Cycle.objects.filter(author=user)

    for cycle in cycles:
        c_post = Post.objects.filter(cycle__title__startswith=cycle.title)
        # print(c_post)

    context = {
        'posts': posts,
        'user': user,
        'u_form': u_form,
        'p_form': p_form,
        'cycles': cycles,
        'c_post': c_post,
    }
    print(c_post)

    return render(request, 'users/profile.html', context)


