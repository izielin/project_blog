from __future__ import absolute_import
from django import forms
from mdeditor.fields import MDTextFormField
from .models import Post, Comment, Document, Cycle
from bootstrap_modal_forms.forms import BSModalForm

CATEGORY_CHOICES = Post.CATEGORY_CHOICES
LEVEL_CHOICES = Post.LEVEL_CHOICES
STATUS_CHOICES = Post.STATUS_CHOICES


class MDEditorForm(forms.Form):
    title = forms.CharField()
    synopsis = forms.CharField()
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="category", initial='', widget=forms.RadioSelect())
    content = MDTextFormField()


class CommentForm(BSModalForm):
    class Meta:
        model = Comment
        fields = ['text']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'document']


class CycleForm(BSModalForm):
    post = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=((x.id, x.title) for x in Post.objects.all()))

    class Meta:
        model = Cycle
        fields = ['title', 'description', 'post']
