from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost
from config import settings
from utils import TitleMixin


class BlogPostCreateView(TitleMixin, CreateView):
    model = BlogPost
    fields = ('title', 'body', 'img_preview',)
    success_url = reverse_lazy('blog:posts')
    title = 'Форма'


class BlogPostListView(TitleMixin, ListView):
    model = BlogPost
    title = 'Блог'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostDetailView(TitleMixin, DetailView):
    model = BlogPost
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_title(self):
        return self.object.title

    def get_object(self, queryset=None):
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


class BlogPostUpdateView(TitleMixin, UpdateView):
    model = BlogPost
    fields = ('title', 'body', 'img_preview',)
    title = 'Редактирование поста'

    def get_success_url(self):
        blog_post = self.get_object()
        return reverse('blog:view_post', args=[blog_post.slug])


class BlogPostDeleteView(TitleMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:posts')
    title = 'Удаление поста'
