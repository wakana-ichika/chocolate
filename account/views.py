from django.shortcuts import render
from django.urls import reverse_lazy
import urllib.parse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth import login, views as auth_v
from .forms import AccountCreate
from .models import Cart, User
from store.session_cart import SessionCartManager


# Create your views here.
# Sign up process.


class AccountInput(generic.FormView):
    form_class = AccountCreate
    template_name = 'account/account-form.html'

    def form_valid(self, form):
        return render(self.request, AccountInput.template_name, {'form': form})


class AccountConfirm(generic.FormView):
    form_class = AccountCreate
    template_name = 'account/account-confirm.html'

    def form_valid(self, form):
        return render(self.request, AccountConfirm.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'account/account-form.html', {'form': form})


class AccountConfirmAfter(generic.CreateView):
    form_class = AccountCreate
    success_url = reverse_lazy('account:account_comp')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.cart = Cart.objects.create()
        new_user.save()

        next_page = self.request.POST.get('next_page', 'home')
        if next_page == 'shopping':
            session_cart = self.request.session[SessionCartManager.kname]
            login(self.request, new_user)
            new_user.cart.import_session(session_cart)
            next_url = reverse_lazy('store:shopping_preview') + '?' + urllib.parse.urlencode({'uname': new_user.name})
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, AccountInput.template_name, {'form': form})


class AccountCompleted(generic.TemplateView):
    template_name = 'account/account-after.html'


# Login process.


class Login(auth_v.LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):

        try:
            session_cart = self.request.session[SessionCartManager.kname]
            self.request.user.cart.import_session(session_cart)
            del self.request.session[SessionCartManager.kname]
        except KeyError:
            return reverse_lazy('store:home')

        next_page = self.request.GET.get('next_page', 'home')
        print(next_page)

        if next_page == 'shopping':
            next_url = reverse_lazy('store:shopping_preview') + '?' + urllib.parse.urlencode(
                {'uname': self.request.user.name}
            )
            return next_url

        else:
            return reverse_lazy('store:home')


class Logout(auth_v.LogoutView):
    next_page = reverse_lazy('store:home')


class Contact(generic.TemplateView):
    template_name = 'account/contact.html'