from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime, timezone
from django.http import HttpResponse
from django.views import View
import os
from django.conf import settings

#from configuration import settings

from .models import *
from .forms import *

import random
import docker
client = docker.from_env()


# home page html theme for reference
class Homepage(TemplateView):
    template_name = 'landing_page/index.html'


# our landing page
class LandingPage(TemplateView):
    template_name = 'landing_page/index.html'

# Redirect for vue dashboard
class FrontendView(View):
    def get(self, request):
        return redirect("vuehome/")
    def post(self, request):
        return redirect("vuehome/")

# registration
class RegisterView(FormView, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_invalid(self, form):
        return super().form_invalid(form)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.is_active = True

        organization_name = user.organization_name
        print("Organization Name" + organization_name + "\n")

        if commit:
            print("Saving User:" + user.username)
            user.save()

        return user

# mixin
class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

# mixin
class NextUrlMixin(object):
    default_next = "mainapp:dashboard"

    def get_next_url(self):
        print("Inside NextURLMixin - get_next_url")
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next

# login for all user types
class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm

    template_name = 'registration/login.html'
    default_next = 'mainapp:dashboard'

    def form_valid(self, form):
        print("Form is valid for Login View, going mainapp:dashboard")
        #return redirect("mainapp:dashboard")
        return redirect("/vuehome")


# after login user will be redirect to this page
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        get_user = self.request.user
        if get_user.admin:
            queryset = DockerContainers.objects.all()
        # elif get_user.organization_admin:
        #     queryset = DockerContainers.objects.filter(user__admin=False)
        else:
            # queryset = DockerContainers.objects.filter(user=get_user.id)
            queryset = DockerContainers.objects.filter(user=get_user)
        return queryset

# after login user will be redirect to this page
class AppListView(LoginRequiredMixin, ListView):
    template_name = 'mainapp/app_list.html'
    queryset = App.objects.all()


# upload file
class AppCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mainapp/create_app.html'
    # queryset = UploadFile.objects.all()
    form_class = AppForm
    success_url = reverse_lazy('mainapp:create_new_app')

    def form_valid(self, form):
        form = self.get_form()
        print(form)
        if form.instance.git_repo_url == "":
            pass
        else:
            repo_name = form.instance.git_repo_url
            directory = form.instance.app_name
            from django.conf import settings
            location_4_repo = os.path.join(settings.ADMIN_ROOT, directory)
            if not os.path.exists(location_4_repo):
                os.mkdir(location_4_repo)
            print("Location for repo:\n")
            print(location_4_repo)
            git_clone_cmd = 'git clone {}'.format(repo_name) + ' "' + location_4_repo + '"'
            print("\nGit Clone Command:\n")
            print(git_clone_cmd)
            os.system(git_clone_cmd)
            # os.system('git clone https://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:x-oauth-basic@github.com/jarvis-vandoc/RShiny_TestApp1.git')
        # print(form.instance.upload_shiny_docker_file)
        # form.instance.save()
        from configuration import settings
        # import os
        # print(os.path.join(settings.MEDIA_ROOT, ''))
        # if form.instance.upload_shiny_docker_file:
        # import docker
        # client = docker.from_env()
        # img = client.images.build(path='./', tag='my_docker_image')
        # print(img.id)
        messages.success(self.request, 'App Detail Has Been Saved Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class DockerImageBuilder(View):
    # queryset = App.objects.all()
    # template_name = "mainapp/app_list.html"

    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get('id')
        get_app_name = App.objects.get(id=id_)
        directory = get_app_name.app_name
        location_4_repo = os.path.join(settings.ADMIN_ROOT, directory)
        print(location_4_repo)
        print(location_4_repo+'/Dockerfile')
        dockerfile_location = location_4_repo+'/Dockerfile'
        print(dockerfile_location)
        client.images.build(path=location_4_repo,tag=directory)
        messages.success(self.request, 'Docker Image Build Successfully')
        print(id_)
        get_app_name.active = False
        get_app_name.save()
        return redirect('mainapp:app_list')

# create docker container
class DockerContainersView(CreateView):
    form_class = DockerContainersForm
    template_name = 'mainapp/docker.html'
    success_url = reverse_lazy('mainapp:dashboard')

    def form_valid(self, form):
        form = self.get_form()
        instance = form.save(commit=False)
        user_ob = form.cleaned_data.get("user")

        docker_image = "rocker/shiny-verse"
        sport = 3838
        port = random.randint(100,9999)

        container = client.containers.run(
            docker_image,
            detach = True,
            ports = {
                '{}/tcp'.format(sport): port
            }
        )

        instance.container_id=container.id
        instance.image=docker_image
        instance.names=container.name
        instance.command=user_ob.first_name+user_ob.last_name
        instance.names=container.name

        #instance.ports=port
        instance.ports=self.request.get_host().replace("8000",str(port))
        instance.status='running'
        instance.save()

        DockerUsage.objects.create(
            container=instance
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# update docker containers
class DockerContainersUpdateView(UpdateView):
    form_class = DockerContainersUpdateForm
    template_name = 'mainapp/docker.html'
    success_url = reverse_lazy('mainapp:dashboard')
    queryset = DockerContainers.objects.all()

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')
        return get_object_or_404(DockerContainers, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        id_ = self.kwargs.get('id')
        cont = DockerContainers.objects.get(id=id_)
        # container = client.containers.get(cont.container_id)
        # if form.cleaned_data.get('status') == 'running':
        #     DockerContainers.objects.filter(container_id=cont.container_id).update(status="running")
        #     DockerUsage.objects.create(
        #         container = cont
        #     )
        #     container.restart()
        # elif form.cleaned_data.get('status') == 'stop':
        #     id_ = self.kwargs.get('id')
        #     DockerContainers.objects.filter(container_id=cont.container_id).update(status="stop")
        #     log = DockerUsage.objects.get(
        #         container = cont,
        #         stop_time=None
        #     )
        #     log.stop_time = datetime.now(timezone.utc)
        #     log.uptime = (
        #         (
        #             datetime.now(timezone.utc) - log.start_time
        #         ).total_seconds()
        #     ) / 60
        #     log.charge = log.uptime*10
        #
        #     log.save()
        #
        #     container = client.containers.get(cont.container_id)
        #     container.stop()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# track docker usage
class DockerUsageView(LoginRequiredMixin, ListView):
    template_name = 'mainapp/docker_log.html'

    def get_queryset(self):
        get_user = self.request.user
        if get_user.admin:
            queryset = DockerUsage.objects.filter(container__in=DockerContainers.objects.all())
        elif get_user.organization_admin:
            queryset = DockerUsage.objects.filter(
                container__in=DockerContainers.objects.filter(user__admin=False))
        else:
            queryset = DockerUsage.objects.filter(
                container__in=DockerContainers.objects.filter(
                    user__admin=False, user=get_user.id))
        return queryset

