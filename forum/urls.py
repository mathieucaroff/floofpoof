from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('', views.select_forum_subject, name='select-forum-subject'),
    path('<int:sub_id>/', PostListView.as_view(), name='forum'),
    path('<int:sub_id>/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:sub_id>/post/new/', PostCreateView.as_view(), name='post-create'),
    path('<int:sub_id>/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:sub_id>/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    ]