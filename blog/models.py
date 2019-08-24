from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mdeditor.fields import MDTextField
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from django.conf import settings


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('Django', 'Django'),
        ('Python', 'Python'),
        ('C++', 'C++'),
        ('Graphics', 'Graphics'),
        ('Text Editor', 'TextEditor'),
        ('Spreadsheet', 'Spreadsheet'),
        ('DataBase', 'DataBase'),
        ('Web Design', 'WebDesign'),
    )

    LEVEL_CHOICES = (
        ('Unknown', 'Unknown'),
        ('Advanced', 'Advanced'),
        ('Intermediate', 'Intermediate'),
        ('Basic', 'Basic'),
    )

    STATUS_CHOICES = (
        ('Work In Progress', 'Work-In-Progress'),
        ('Not Approved Yet', 'Not-Approved-Yet'),
        ('Approved', 'Approved'),
    )

    title = models.CharField(max_length=50, unique=True)
    synopsis = models.TextField(max_length=500)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES, default="Unknown")
    content = MDTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authorized = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Not-Approved-Yet")
    numbers_of_entries = models.IntegerField(default=0)
    ratings = GenericRelation(Rating)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Email(models.Model):
    # sender = models.EmailField(max_length=100, default="ecg.vot@gmail.com")
    sender = models.EmailField(max_length=100, default=settings.EMAIL_HOST_USER)
    receivers = models.TextField(max_length=500, default="['test@test.pl']")
    # date_created = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(null=True, blank=True)
    posted = models.BooleanField(default=False)
    # date_posted = models.DateTimeField(editable=False, null=True, blank=True)
    date_posted = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="usernames", max_length=100)
    subject = models.TextField(max_length=100, default="Subject")
    message = models.TextField(max_length=1000, default="message")

    # __posted = None
    # def __init__(self, *args, **kwargs):
    #     super(Email, self).__init__(*args, **kwargs)
    #     self.__posted = self.posted
    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     if self.posted != self.__posted:
    #         # posted changed - do something here
    #     super(Email, self).save(force_insert, force_update, *args, **kwargs)
    #     self.__posted = self.posted

    def get_absolute_url(self):
        return reverse('email-detail', kwargs={'pk': self.pk})

    def __str__(self):
        # return self.subject
        return '%s %s' % (self.subject, self.date_created)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_created = timezone.now()
        if self.posted and self.date_posted==None:
            self.date_posted = timezone.now()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text


class Document(models.Model):
    name = models.CharField(max_length=100, unique=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    postId = models.IntegerField()

    def get_absolute_url(self):
        return reverse('post-upload-detail', kwargs={'pk': self.pk})
