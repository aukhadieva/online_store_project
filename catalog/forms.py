from django import forms

from catalog.models import Product


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductModelForm(StyleMixin, forms.ModelForm):
    BANNED_LIST = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('product_name', 'price', 'category', 'prod_desc', 'image',)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        if cleaned_data in self.BANNED_LIST:
            raise forms.ValidationError('Название товара содержат недопустимые слова')

        return cleaned_data

    def clean_prod_desc(self):
        cleaned_data = self.cleaned_data['prod_desc']
        if cleaned_data in self.BANNED_LIST:
            raise forms.ValidationError('Описание товара содержат недопустимые слова')

        return cleaned_data
