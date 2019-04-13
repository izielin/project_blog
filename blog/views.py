from django.shortcuts import render

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog post number one',
        'content': 'First post content',
        'date_posted': 'September 12, 2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog post number two',
        'content': 'Second post content',
        'date_posted': 'September 17, 2018',
    }

]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
