import json

from django.shortcuts import render

from catalog.models import Contact, Product


def index(request):
    product = [product.product_name for product in Product.objects.all()]
    products = product[0:5]
    return render(request, 'catalog/index.html', context={'products': products})


def contacts(request):
    contact = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contacts_dict = {'contacts_data': [{'name': name, 'email': email, 'message': message}]}
        with open('contacts_data.json', 'w') as j_file:
            json.dump(contacts_dict, j_file, indent=4, ensure_ascii=False)
    return render(request, 'catalog/contacts.html', context={'contact': contact})
