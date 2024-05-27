from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version
from utils import StyleMixin


class ProductForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.
    """
    BANNED_LIST = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('product_name', 'price', 'category', 'prod_desc', 'image', 'is_published')

    def clean_product_name(self):
        """
        Проверяет название продукта на наличие недопустимых слов.
        """
        cleaned_data = self.cleaned_data['product_name']
        for word in cleaned_data:
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Название товара содержат недопустимые слова')

        return cleaned_data

    def clean_prod_desc(self):
        """
        Проверяет описание продукта на наличие недопустимых слов.
        """
        cleaned_data = self.cleaned_data['prod_desc']
        for word in cleaned_data:
            if word in self.BANNED_LIST:
                raise forms.ValidationError('Описание товара содержат недопустимые слова')

        return cleaned_data


class VersionForm(StyleMixin, forms.ModelForm):
    """
    Форма для создания и редактирования версий продуктов.
    """

    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'is_current')

    def clean_is_current(self):
        """
        Проверяет наличие текущей версии продукта.
        Если такая есть, то поднимается ValidationError.
        """
        is_current = self.cleaned_data.get('is_current')
        if is_current and Version.objects.filter(product=self.instance.product, is_current=True).exclude(
                id=self.instance.id).exists():
            raise ValidationError("Только одна версия продукта может быть текущей.")
        return is_current

    def save(self, commit=True):
        """
        Сохраняет версию продукта.
        """
        instance = super().save(commit=False)
        if instance.is_current:
            Version.objects.filter(product=instance.product, is_current=True).exclude(id=instance.id).update(
                is_current=False)
        if commit:
            instance.save()
        return instance
