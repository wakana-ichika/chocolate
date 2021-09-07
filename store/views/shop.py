from django import forms
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from account.models import Shopping
from account.auth_mixin import GetOnlyYouMixin, PostOnlyYouMixin


@method_decorator(never_cache, name='dispatch')
class ShoppingPreview(GetOnlyYouMixin, generic.TemplateView):
    template_name = 'store/shopping/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.user.cart
        context['total_price'] = cart.total_price()
        lis = [
            {'goods': unit.goods.name,
             'goods_pk': unit.goods.pk,
             'add_tax': unit.goods.add_tax,
             'price': unit.goods.add_tax * unit.quantity,
             'quantity': unit.quantity,
             'unit_pk': unit.pk,
             } for unit, price in zip(cart.units.all(), cart.small())]

        context['small'] = lis
        return context


@method_decorator(never_cache, name='dispatch')
class ShoppingProcess(PostOnlyYouMixin, generic.FormView):
    form_class = forms.Form
    success_url = reverse_lazy('store:shopping_done')

    def form_valid(self, form):
        user = self.request.user
        for unit in user.cart.units.all():
            Shopping.objects.create(user_pk=user, goods_pk=unit.goods, how_many=unit.quantity)
        user.cart.units.clear()
        return super().form_valid(form)


class ShoppingDone(generic.TemplateView):
    template_name = 'store/shopping/done.html'
