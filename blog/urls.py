from django.urls import path
from .views import (
    PostUpdateView,
    PostDeleteView,
    CommentDeleteView,
    DownloadDeleteView,
    MDEditorFormView,
    ShowView,
)
from . import views

urlpatterns = [
    path('about/', views.about, name='blog-about'),
    path('no-authorized/', views.posts_no_authorized, name='post-no-authorized'),
    path('post/<int:pk>/', ShowView.as_view(), name='post-detail'),
    path('post/new/', MDEditorFormView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/upload/', views.model_form_upload, name='post-upload'),
    path('download/<int:pk>', DownloadDeleteView.as_view(), name='upload-delete'),
    path('post/<int:pk>/download/', views.download, name='post-download'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]