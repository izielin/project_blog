from __future__ import absolute_import

from django import forms

from mdeditor.fields import MDTextFormField
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.models import User

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


class MDEditorForm(forms.Form):
    title = forms.CharField()
    synopsis = forms.CharField(required=True)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="category", initial='', widget=forms.Select(), required=True)
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="level", initial='', widget=forms.Select(), required=True)
    content = MDTextFormField()


class MDEditorModleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
