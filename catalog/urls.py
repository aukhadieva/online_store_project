from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, product, listing

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:product_id>', product, name='product'),
    path('category/<int:category_id>', listing, name='category'),
    path('store/', listing, name='store'),
    path('store/<int:page_number>', listing, name='paginator')
]
