from django.views import generic
from django import forms
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect

from store.session_cart import SessionCartManager


@method_decorator(never_cache, name='dispatch')
class SessionCartContent(generic.FormView):
    template_name = 'store/cart.html'
    form_class = forms.Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get(SessionCartManager.kname, [])
        context['total_price'] = SessionCartManager.total_price(cart)
        context['cart_list'] = SessionCartManager.rendering_unit(cart)
        return context

    def form_valid(self, form):
        return render(self.request, SessionCartContent.template_name, {'form': form})


class SessionAddToCart(generic.RedirectView):
    url = reverse_lazy('store:sessioncart_content')

    def post(self, request, *args, **kwargs):
        goods_pk = request.POST['goods_pk']
        quantity = request.POST['quantity']
        cart = request.session.get(SessionCartManager.kname, [])
        cart = SessionCartManager.add_unit(cart, goods_pk, quantity)
        request.session[SessionCartManager.kname] = cart
        return super().post(request, *args, **kwargs)


class SessionMinusToCart(generic.RedirectView):
    url = reverse_lazy('store:sessioncart_content')

    def post(self, request, *args, **kwargs):
        goods_pk = request.POST['goods_pk']
        cart = self.request.session.get(SessionCartManager.kname)
        cart = SessionCartManager.minus_unit(cart, goods_pk)
        self.request.session[SessionCartManager.kname] = cart

        return super().post(request, *args, **kwargs)


class SessionCartDelete(generic.FormView):
    form_class = forms.Form
    success_url = reverse_lazy('store:sessioncart_content')

    def form_valid(self, form):
        cart = self.request.session[SessionCartManager.kname]
        delete_goods_pk = int(self.request.POST['goods_pk'])
        cart = SessionCartManager.delete_unit(cart, delete_goods_pk)
        self.request.session[SessionCartManager.kname] = cart
        return super(SessionCartDelete, self).form_valid(form)
