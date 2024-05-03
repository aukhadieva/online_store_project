from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (index, ContactTemplateView, ProductDetailView, ProductListView, BlogPostCreateView,
                           BlogPostListView, BlogPostDetailView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('view_product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('store/', ProductListView.as_view(), name='store'),
    path('create_post/', BlogPostCreateView.as_view(), name='create_post'),
    path('posts/', BlogPostListView.as_view(), name='posts'),
    path('view_post/<int:pk>', BlogPostDetailView.as_view(), name='view_post')
]
