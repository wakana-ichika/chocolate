from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('account-input/', views.AccountInput.as_view(), name='account_input'),
    path('account-confirm/', views.AccountConfirm.as_view(), name='account_confirm'),
    path('account-after/', views.AccountConfirmAfter.as_view(), name='account_after'),
    path('account-completed/', views.AccountCompleted.as_view(), name='account_comp'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('contact/', views.Contact.as_view(), name='contact')
]