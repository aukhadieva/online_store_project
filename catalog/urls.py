from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, ContactTemplateView, ProductDetailView, listing

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('category/<int:category_id>', listing, name='category'),
    path('store/', listing, name='store'),
    path('store/<int:page_number>', listing, name='paginator')
]
