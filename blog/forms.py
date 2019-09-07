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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['posts'].queryset = Post.objects.filter(author=user)

    class Meta:
        model = Cycle
        fields = ['title', 'description', 'posts']
        widgets = {
            'posts': forms.CheckboxSelectMultiple(),
        }
