from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.forms import BlogPostForm
from blog.models import BlogPost
from config import settings
from utils import TitleMixin


class BlogPostCreateView(TitleMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:posts')
    title = 'Форма'
    permission_required = 'blog.add_blogpost'


class BlogPostListView(TitleMixin, ListView):
    model = BlogPost
    title = 'Блог'

    def get_queryset(self, *args, **kwargs):
        """
        Отображает только посты с флагом is_published.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostDetailView(TitleMixin, DetailView):
    model = BlogPost
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_title(self):
        """
        Возвращает заголовок страницы.
        """
        return self.object.title

    def get_object(self, queryset=None):
        """
        Увеличивает количество просмотров поста
        и отправляет письмо автору поста при 100 просмотрах.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail('Поздравляем!',
                      'Ваш пост набрал 100 просмотров!',
                      settings.EMAIL_HOST_USER,
                      ['saratova.olga.s@mail.ru'],
                      fail_silently=False, )
        return self.object


class BlogPostUpdateView(TitleMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    title = 'Редактирование поста'
    permission_required = 'blog.change_blogpost'

    def get_success_url(self):
        """
        Формирует url для перенаправления после редактирования поста.
        """
        blog_post = self.get_object()
        return reverse('blog:view_post', args=[blog_post.slug])


class BlogPostDeleteView(TitleMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:posts')
    title = 'Удаление поста'
    permission_required = 'blog.delete_blogpost'
