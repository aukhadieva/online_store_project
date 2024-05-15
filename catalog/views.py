from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Contact, Product, Category, Version
from utils import TitleMixin


def index(request):
    context = {'title': 'Главная',
               'object_list': Product.objects.all()[:3]}
    return render(request, 'catalog/index.html', context)


class ProductCreateView(TitleMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:store')
    title = 'Создание продукта'


class ProductUpdateView(TitleMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:store')
    title = 'Редактирование продукта'

    def get_success_url(self):
        product = self.get_object()
        return reverse_lazy('catalog:view_product', args=[product.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST' and Version:
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(TitleMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:store')
    title = 'Удаление продукта'


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
        queryset = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['categories'] = Category.objects.all()
        return context_data

        # вариант 1 - выводит только один товар (чья версия была изменена на активную)
        # versions = Version.objects.filter(is_current=True)
        # for version in versions:
        #     products = Product.objects.filter(version=version)
        #     context_data['object_list'] = products.all()
        # return context_data

        # вариант 2 - не работает
        # for product in context_data.get('object_list'):
        #     product.version = product.version.filter(is_current=True).first()
        # return context_data


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
