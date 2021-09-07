from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class AccountCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'furigana', 'tell', 'email',
                  'post_code', 'address1', 'address2', 'address3')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '山田花子'}),
            'furigana': forms.TextInput(attrs={'placeholder': 'ヤマダハナコ'}),
            'tell': forms.NumberInput(attrs={'placeholder': '080XXXXOOOO'}),
            'email': forms.TextInput(attrs={'placeholder': 'aaaa@email.co.jp'}),
            'post_code': forms.TextInput(attrs={'class': 'p-postal-code', 'placeholder': '4510045'}),
            'address1': forms.TextInput(attrs={'class': 'p-region', 'placeholder': '愛知県'}),
            'address2': forms.TextInput(attrs={'class': 'p-locality p-street-address p-extended-address',
                                               'placeholder': '名古屋市西区名駅1-2-3'}),
            'address3': forms.TextInput(attrs={'placeholder': '海鮮マンションAB号室'})
        }

