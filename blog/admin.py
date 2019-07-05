from django.contrib import admin
from .models import Post, Comment
from django.db import models

# Register your models here.
from . import models as demo_models
from mdeditor.widgets import MDEditorWidget


class ExampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(demo_models.Post, ExampleModelAdmin)

# admin.site.register(FileUploadUrl)
admin.site.register(Comment)
