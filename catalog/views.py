from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductModelForm
from catalog.models import Contact, Product, Category
from utils import TitleMixin


def index(request):
    context = {'title': 'Главная',
               'object_list': Product.objects.all()[:3]}
    return render(request, 'catalog/index.html', context)


class ProductCreateView(TitleMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy('catalog:store')
    title = 'Создание продукта'


class ProductUpdateView(TitleMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy('catalog:store')
    title = 'Редактирование продукта'


class ProductDeleteView(TitleMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:store')
    title = 'Удаление продукта'


class ContactTemplateView(TitleMixin, TemplateView):
    template_name = 'catalog/contacts.html'
    title = 'Обратная связь'

    def post(self, request):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            new_contact = Contact.objects.create(name=name, email=email, message=message)
            new_contact.save()
        return render(self.request, self.template_name)


class ProductDetailView(TitleMixin, DetailView):
    model = Product

    def get_title(self):
        return self.object.product_name


class ProductListView(TitleMixin, ListView):
    model = Product
    paginate_by = 3
    template_name = "catalog/product_list.html"
    title = 'Каталог'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
