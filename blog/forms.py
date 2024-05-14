from django import forms

from blog.models import BlogPost


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogPostForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'img_preview',)
