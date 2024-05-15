from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (index, ContactTemplateView, ProductDetailView, ProductListView, ProductCreateView,
                           ProductUpdateView, ProductDeleteView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('create_product', ProductCreateView.as_view(), name='create_product'),
    path('edit_product/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('view_product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('store/', ProductListView.as_view(), name='store'),
    path('store/category/<int:category_id>', ProductListView.as_view(), name='category'),
]
