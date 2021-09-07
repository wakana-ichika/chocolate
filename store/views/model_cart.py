from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import ModelFormMixin

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from account.auth_mixin import OnlyYouMixin, PostOnlyYouMixin
from account.models import User
from goods.models import Goods
from store.models import CartUnit
from store.forms import CartUnitForm


@method_decorator(never_cache, name='dispatch')
class ModelCartContent(OnlyYouMixin, generic.DetailView):
    model = User
    context_object_name = 'cart'
    template_name = 'store/cart.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj.cart

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


class ModelAddToCart(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))

    def post(self, request, *args, **kwargs):
        user = request.user
        goods_pk = request.POST['goods_pk']
        quantity = request.POST['quantity']
        unit_add = CartUnit(goods=Goods.objects.get(pk=goods_pk), quantity=int(quantity))
        user.cart.add_unit(unit_add)
        return super().post(request, *args, **kwargs)


class ModelMinusToCart(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))

    def post(self, request, *args, **kwargs):
        user = request.user
        goods_pk = request.POST['goods_pk']
        quantity = request.POST['quantity']
        unit_add = CartUnit(goods=Goods.objects.get(pk=goods_pk), quantity=int(quantity))
        user.cart.minus_unit(unit_add)
        return super().post(request, *args, **kwargs)


class ModelCartDelete(PostOnlyYouMixin, generic.DeleteView):
    model = CartUnit

    def get_object(self, queryset=None):
        unit_pk = self.request.POST['unit_pk']
        return CartUnit.objects.get(id=unit_pk)

    def get_success_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))