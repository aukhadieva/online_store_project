from django.urls import path

from blog.apps import BlogConfig
from blog.views import (BlogPostCreateView,
                        BlogPostListView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView)

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='posts'),
    path('view_post/<slug:slug>', BlogPostDetailView.as_view(), name='view_post'),
    path('create_post/', BlogPostCreateView.as_view(), name='create_post'),
    path('edit_post/<int:pk>', BlogPostUpdateView.as_view(), name='edit_post'),
    path('delete_post/<int:pk>', BlogPostDeleteView.as_view(), name='delete_post'),
]
