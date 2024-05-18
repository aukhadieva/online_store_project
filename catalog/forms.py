from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version


class StyleMixin:
    """
    Миксин для стилизации форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.
    """
    BANNED_LIST = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('product_name', 'price', 'category', 'prod_desc', 'image',)

    def clean_product_name(self):
        """
        Проверяет название продукта на наличие недопустимых слов.
        """
        cleaned_data = self.cleaned_data['product_name']
        for word in cleaned_data.split():
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Название товара содержат недопустимые слова')

        return cleaned_data

    def clean_prod_desc(self):
        """
        Проверяет описание продукта на наличие недопустимых слов.
        """
        cleaned_data = self.cleaned_data['prod_desc']
        for word in cleaned_data.split():
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Описание товара содержат недопустимые слова')

        return cleaned_data


class VersionForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования версий продуктов.
    """

    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'product', 'is_current')

    def clean_is_current(self):
        """
        Проверяет наличие текущей версии продукта.
        Если такая есть, то поднимается ValidationError
        (сообщение будет отображено пользователю при отправке формы).
        """
        is_current = self.cleaned_data.get('is_current')
        if is_current:
            if Version.objects.filter(is_current=True).exists():
                raise ValidationError("Существует другая текущая версия. Она будет деактивирована.")
        return is_current

    def save(self, commit=True):
        """
        Обновляет флаги текущей версии продукта.
        Если новая версия устанавливается как текущая,
        все предыдущие версии для данного продукта деактивируются.
        """
        instance = super().save(commit=False)
        if instance.is_current:
            Version.objects.filter(product=instance.product, is_current=True).update(is_current=False)
        if commit:
            instance.save()
        return instance
