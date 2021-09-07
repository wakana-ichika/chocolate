from django.urls import path
from store import views as store_v

app_name = 'store'

urlpatterns = [
    path('', store_v.Home.as_view(), name='home'),
    path('seasonal/', store_v.Seasonal.as_view(), name='seasonal'),
    path('chocolate/', store_v.Chocolate.as_view(), name='chocolate'),
    path('baked/', store_v.Baked.as_view(), name='baked'),
    path('anniversary/', store_v.Anniversary.as_view(), name='anniversary'),
    path('sessioncontent/', store_v.SessionCartContent.as_view(), name='sessioncart_content'),
    path('add_sessioncart/', store_v.SessionAddToCart.as_view(), name='add_sessioncart'),
    path('minus_sessioncart/', store_v.SessionMinusToCart.as_view(), name='minus_sessioncart'),
    path('delete_sessioncart/', store_v.SessionCartDelete.as_view(), name='delete_sessioncart'),
    path('modelcontent/<int:pk>/', store_v.ModelCartContent.as_view(), name='modelcart_content'),
    path('add_modelcart/', store_v.ModelAddToCart.as_view(), name='add_modelcart'),
    path('minus_modelcart/', store_v.ModelMinusToCart.as_view(), name='minus_modelcart'),
    path('delete_modelcart/', store_v.ModelCartDelete.as_view(), name='modelcart_delete'),
    path('shopping/shopping_preview/', store_v.ShoppingPreview.as_view(), name='shopping_preview'),
    path('shopping/shopping_process/', store_v.ShoppingProcess.as_view(), name='shopping_process'),
    path('shopping/shopping_done/', store_v.ShoppingDone.as_view(), name='shopping_done')
]
