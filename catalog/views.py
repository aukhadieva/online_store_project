import json

from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        review = request.POST.get('review')
        print(review)
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contacts_dict = {'contacts_data': [{'name': name, 'email': email, 'message': message}]}
        with open('contacts_data.json', 'w') as j_file:
            json.dump(contacts_dict, j_file, indent=4, ensure_ascii=False)
    return render(request, 'catalog/contacts.html')
