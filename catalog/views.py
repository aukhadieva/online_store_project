from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Contact, Product, Category, Version
from utils import TitleMixin


def index(request):
    """
    Главная страница с продуктами.
    """
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
        """
        Возвращает URL, на который должен быть перенаправлен пользователь после успешной обработки формы.
        """
        product = self.get_object()
        return reverse_lazy('catalog:view_product', args=[product.pk])

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст форму с версиями продукта.
        """
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет ее.
        """
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(TitleMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:store')
    title = 'Удаление продукта'


class ProductDetailView(TitleMixin, DetailView):
    model = Product

    def get_title(self):
        """
        Возвращает заголовок страницы.
        """
        return self.object.product_name


class ProductListView(TitleMixin, ListView):
    model = Product
    paginate_by = 3
    template_name = "catalog/product_list.html"
    title = 'Каталог'

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает список продуктов, отфильтрованных по категории (при применении фильтра).
        """
        queryset = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *args, **kwargs):
        """
        Добавляет в контекст список категорий и переопределяет список продуктов.
        """
        # получаем текущий контекст
        context_data = super().get_context_data(*args, **kwargs)
        # добавляем категории в контекст
        context_data['categories'] = Category.objects.all()

        # Получаем текущий список продуктов из `context_data`
        products = context_data.get('object_list')
        # для каждого продукта ищем текущую версию (`is_current=True`)
        # и сохраняем ее в новое поле `current_version` у объекта продукта.
        # Это поле добавляется динамически и не сохраняется в базе данных.
        for product in products:
            current_version = product.version.filter(is_current=True).first()
            if current_version:
                product.current_version = current_version
        # возвращаем обновленный контекст
        return context_data


class ContactTemplateView(TitleMixin, TemplateView):
    template_name = 'catalog/contacts.html'
    title = 'Обратная связь'

    def post(self, request):
        """
        Обрабатывает отправку формы обратной связи.
        """
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            new_contact = Contact.objects.create(name=name, email=email, message=message)
            new_contact.save()
        return render(self.request, self.template_name)
