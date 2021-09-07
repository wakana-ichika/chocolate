from django import forms
from .models import CartUnit


class CartUnitForm(forms.ModelForm):
    class Meta:
        model = CartUnit
        fields = ('quantity',)
