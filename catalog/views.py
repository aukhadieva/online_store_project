import json

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from catalog.models import Contact, Product, Category


def index(request):
    context = {'title': 'Главная',
               'object_list': Product.objects.all()[:3],
               'category_list': Category.objects.all()}
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category_id = Category.objects.get(category_name=category).id
        prod_desc = request.POST.get('prod_desc')
        new_book = Product.objects.create(product_name=product_name,
                                          price=price,
                                          category=Category.objects.get(pk=category_id),
                                          prod_desc=prod_desc)
        new_book.save()
    return render(request, 'catalog/index.html', context)


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            new_contact = Contact.objects.create(name=name, email=email, message=message)
            new_contact.save()
        return render(self.request, self.template_name)


def product(request, product_id):
    object = get_object_or_404(Product, pk=product_id)
    return render(request, 'catalog/product.html', {'object': object})


def listing(request, category_id=None, page_number=1):
    category_list = Category.objects.all()
    if category_id:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3)
    page_object = paginator.get_page(page_number)

    context = {'title': 'Каталог',
               'category_list': category_list,
               'page_object': page_object}
    return render(request, 'catalog/store.html', context)
