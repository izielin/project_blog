from django.urls import path
from .views import (
    PostUpdateView,
    PostDeleteView,
    CommentDeleteView,
    DownloadDeleteView,
    MDEditorFormView,
    ShowView,
    CommentCreateView,
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post_list/', views.post_list, name='post-list'),
    path('post/<int:pk>/', ShowView.as_view(), name='post-detail'),
    path('post/new/', MDEditorFormView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/upload/', views.model_form_upload, name='post-upload'),
    path('no-authorized/', views.posts_no_authorized, name='post-no-authorized'),
    path('post/<int:pk>/download/', views.download, name='post-download'),
    path('download/<int:pk>', DownloadDeleteView.as_view(), name='upload-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment_to_post'),
    path('delete_comment/<int:pk>', CommentDeleteView.as_view(), name='comment-delete'),
]