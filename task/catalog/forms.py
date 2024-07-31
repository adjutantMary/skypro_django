import re

from .models import *
from django import forms
from django.forms import BooleanField


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.item():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "forms-control"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('product_name', '')
        description = cleaned_data.get('product_description', '')

        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция',
            'радар'
        ]

        for word in forbidden_words:
            if re.search(re.escape(word), name.casefold()):
                raise forms.ValidationError(f'Название содержит запрещенное слово "{word}"')

            if re.search(re.escape(word), description.casefold()):
                raise forms.ValidationError(f'Описание содержит запрещенное слово "{word}"')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = [
            'product', 'version_number',
            'version_name', 'is_current'
        ]
        labels = {
            'version_number': 'Номер версии',
            'version_name': 'Название версии',
            'is_current': 'Текущая версия'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["version_number"].widget.attrs.update({'class': 'form-control'})
            self.fields['version_name'].widget.attrs.update({'class': 'form-control'})
            self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})

