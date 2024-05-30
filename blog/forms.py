from django import forms

from blog.models import BlogPost
from utils import StyleMixin


class BlogPostForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования поста в блоге.
    """

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'img_preview',)
