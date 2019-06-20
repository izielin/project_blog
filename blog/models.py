from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


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

    title = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=200, default="")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})