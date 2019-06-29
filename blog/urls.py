from django.urls import path
from .views import (
    PostListView,
    # PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    DownloadDeleteView
)
from . import views

urlpatterns = [
    path('about/', views.about, name='blog-about'),
    # path('about/', PostListView.as_view(), name='blog-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('model/', views.mdeditor_model_form_view, name='mdeditor-model-form'),
    path('post/<int:pk>/', views.show_view, name='post-detail'),
    path('post/new/', views.mdeditor_form_view, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/upload/', views.simple_upload, name='post-upload'),
    path('download/<int:pk>', DownloadDeleteView.as_view(), name='upload-delete'),
    path('post/<int:pk>/download/', views.download, name='post-download'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]