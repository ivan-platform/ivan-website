from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import *

class LoginForm(forms.Form):
    username = forms.EmailField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.warning(request, "Invalid credentials")
            raise forms.ValidationError('Invalid credentials')

        login(request, user)
        self.user = user
        return data


# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     test1 = forms.BooleanField(label='Shiny app 1')
#     test2 = forms.BooleanField(label='Shiny app 2')
#     test3 = forms.BooleanField(label='Shiny app 3')
#
#     class Meta:
#         model = User
#         fields = ('username', 'mobile', 'first_name', 'last_name')
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             username_exist_error = "This username is already exists"
#             raise forms.ValidationError(mark_safe(username_exist_error))
#         return username
#
#     def clean_mobile(self):
#         mobile = self.cleaned_data.get('mobile')
#         mobile = int(mobile)
#         return mobile
#
#     def clean_test1(self):
#         test1 = self.cleaned_data.get('test1')
#         username = self.cleaned_data.get('username')
#         # print(test1)
#         # import random
#         # docker_image = "rocker/shiny-verse"
#         # port = random.randint(100, 9999)
#         # DockerContainers.objects.create(
#         #     user=username,
#         #     image=docker_image,
#         #     command='command',
#         #     status='running',
#         #     port=port,
#         #     name=username,
#         # )
#         return test1
#
#     def clean_test2(self):
#         test2 = self.cleaned_data.get('test2')
#         return test2
#
#     def clean_test3(self):
#         test3 = self.cleaned_data.get('test3')
#         return test3
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(_("Passwords not match"))
#         return password2
#
#     def save(self, commit=True):
#         user = super(RegisterForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.is_active = True
#
#         if commit:
#             user.save()
#             docker_image = "rocker/shiny-verse"
#             test1 = self.cleaned_data.get('test1')
#             test2 = self.cleaned_data.get('test2')
#             test3 = self.cleaned_data.get('test3')
#             if test1 is not None:
#                 import random
#                 port = random.randint(999, 9999)
#                 DockerContainers.objects.create(
#                     user=user,
#                     image=docker_image,
#                     command='command not available',
#                     status='stop',
#                     ports=port,
#                     names=test1,
#                 )
#             if test2 is not None:
#                 import random
#                 port = random.randint(999, 9999)
#                 DockerContainers.objects.create(
#                     user=user,
#                     image=docker_image,
#                     command='command not available',
#                     status='stop',
#                     ports=port,
#                     names=test2,
#                 )
#             if test3 is not None:
#                 import random
#                 port = random.randint(999, 9999)
#                 DockerContainers.objects.create(
#                     user=user,
#                     image=docker_image,
#                     command='command not available',
#                     status='stop',
#                     ports=port,
#                     names=test3,
#                 )
#             return user


class DockerContainersUpdateForm(forms.ModelForm):
    class Meta:
        model = DockerContainers
        fields = ['status']


class DockerContainersForm(forms.ModelForm):
    class Meta:
        model = DockerContainers
        fields = ['user']