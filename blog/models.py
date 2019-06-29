from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('Django', 'Django'),
        ('Python', 'Python'),
        ('C++', 'C++'),
        ('Graphics', 'Graphics'),
        ('Word', 'Word'),
        ('Excel', 'Excel'),
        ('DataBase', 'DataBase'),
        ('Html & css', 'Html&css'),
        ('JavaScript', 'JavaScript'),
        ('Java', 'Java'),
    )

    LEVEL_CHOICES = (
        ('Advanced', 'Advanced'),
        ('Intermediate', 'Intermediate'),
        ('Basic', 'Basic'),
    )

    title = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES, default="")
    content = MDTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = GenericRelation(Rating, related_query_name='foos')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('add_comment_to_comment', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text


class FileUploadUrl(models.Model):
    fileName = models.CharField(max_length=255, default="")
    url = models.CharField(max_length=255)
    postId = models.IntegerField()

    def get_absolute_url(self):
        return reverse('post-upload-detail', kwargs={'pk': self.pk})
