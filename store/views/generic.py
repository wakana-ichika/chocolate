from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import ModelFormMixin

from goods.models import Goods
from store.forms import CartUnitForm

import random

# Create your views here.


class Home(generic.ListView):
    model = Goods
    template_name = 'store/index.html'
    context_object_name = 'goods_list'

    def get_context_data(self, **kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        goods = Goods.objects.all()
        lis = []
        pick_up = []

        for i in range(10):
            item = random.choice(goods)
            lis.append(item)
        for i in range(3):
            for list_item in lis:
                if pick_up.count(list_item) == 0 and len(pick_up) < 3:
                    pick_up.append(list_item)
                    continue

        context['pick_up'] = pick_up
        return context


class Seasonal(generic.ListView):
    model = Goods
    template_name = 'store/seasonal.html'
    context_object_name = 'goods_list'


class Chocolate(generic.ListView):
    model = Goods
    template_name = 'store/chocolate.html'
    context_object_name = 'goods_list'


class Baked(generic.ListView):
    model = Goods
    template_name = 'store/baked.html'
    context_object_name = 'goods_list'


class Anniversary(generic.ListView):
    model = Goods
    template_name = 'store/anniversary.html'
    context_object_name = 'goods_list'
