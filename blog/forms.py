from django import forms

from blog.models import BlogPost
from utils import StyleMixin


class BlogPostForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'img_preview',)
