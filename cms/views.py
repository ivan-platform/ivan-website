from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.utils.http import is_safe_url
from django.views.generic.edit import FormView

from .models import *
from .forms import *
# Create your views here.


class Homepage(TemplateView):
    template_name = 'cms/index.html'

class LandingPage(TemplateView):
    template_name = 'landing_page/index.html'

class LoginViewTest(TemplateView):
    template_name = 'registration/login.html'


from django.contrib.auth.forms import AuthenticationForm

class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "cms:home"

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    print("Login ----")
    template_name = 'registration/login.html'
    default_next = 'cms:home'

    def form_valid(self, form):
        return redirect("cms:home")

