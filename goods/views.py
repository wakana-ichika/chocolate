from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from .models import GoodsGroup, Goods
from .forms import GoodsGroupForm, GoodsForm
from store.forms import CartUnitForm

# Create your views here.


class GoodsGroupCreate(generic.CreateView):
    model = GoodsGroup
    form_class = GoodsGroupForm
    template_name = 'goods/group_create.html'
    success_url = '/goods/group_create'


class GoodsCreate(generic.CreateView):
    model = Goods
    form_class = GoodsForm
    template_name = 'goods/goods_create.html'
    success_url = '/goods/goods_create'


class GoodsDetail(ModelFormMixin, generic.DetailView):
    model = Goods
    template_name = 'goods/goods_detail.html'
    form_class = CartUnitForm

    def form_valid(self, form):
        return render(self.request, 'goods/goods_detail.html', {'form': form})
