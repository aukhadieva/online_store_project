from django.urls import path

from catalog.views import index, contacts


app_name = 'catalog'

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts')
]
