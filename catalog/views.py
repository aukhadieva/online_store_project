from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.templatetags.pytils_translit import slugify

from catalog.models import Contact, Product, Category, BlogPost


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


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
    paginate_by = 3


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'body', 'img_preview',)
    success_url = reverse_lazy('catalog:posts')


class BlogPostListView(ListView):
    model = BlogPost
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail('Поздравляем!',
                      'Ваш пост набрал 100 просмотров!',
                      'olyaramilya@yandex.ru',
                      ['olyaramilya@yandex.ru', 'sarole4ka@gmail.com'],
                      fail_silently=False,)
        return self.object


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'body', 'img_preview',)

    def get_success_url(self):
        return reverse('catalog:view_post', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:posts')
