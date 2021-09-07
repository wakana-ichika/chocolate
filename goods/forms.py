from django import forms
from .models import GoodsGroup, Goods


class GoodsGroupForm(forms.ModelForm):
    class Meta:
        model = GoodsGroup
        fields = '__all__'


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ('name', 'management_code', 'price', 'release_data', 'release_flag', 'text', 'image',
                  'state_flag', 'group')

