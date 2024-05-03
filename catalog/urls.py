from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, ContactTemplateView, ProductDetailView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('view_product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('store/', ProductListView.as_view(), name='store'),
]
