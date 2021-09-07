from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('group_create/', views.GoodsGroupCreate.as_view(), name='group_create'),
    path('goods_create/', views.GoodsCreate.as_view(), name='goods_create'),
    path('goods_detail/<int:pk>', views.GoodsDetail.as_view(), name='goods_detail'),
]