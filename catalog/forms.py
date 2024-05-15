from django import forms

from catalog.models import Product, Version


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleMixin, forms.ModelForm):
    BANNED_LIST = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('product_name', 'price', 'category', 'prod_desc', 'image',)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        for word in cleaned_data.split():
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Название товара содержат недопустимые слова')

        return cleaned_data

    def clean_prod_desc(self):
        cleaned_data = self.cleaned_data['prod_desc']
        for word in cleaned_data.split():
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Описание товара содержат недопустимые слова')

        return cleaned_data


class VersionForm(forms.ModelForm):
    version_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название версии')
    version_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Номер версии')
    is_current = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Признак текущей версии', required=False)

    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'product', 'is_current')

    def clean_is_current(self):
        cleaned_data = self.cleaned_data['is_current']
        versions = Version.objects.filter(is_current=True)
        for version in versions:
            if version.is_current:
                version.is_current = False
                version.save()

        return cleaned_data
