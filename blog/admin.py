from django.contrib import admin
from .models import Post, FileUploadUrl, Comment

admin.site.register(Post)
admin.site.register(FileUploadUrl)
admin.site.register(Comment)
