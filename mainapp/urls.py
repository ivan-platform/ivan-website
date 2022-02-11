from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    url('^home$', views.Homepage.as_view(), name='home'), # home page html theme for reference
    url('^$', views.LandingPage.as_view(), name='index'), # our landing page
    url('^vuehome$', views.FrontendView.as_view(), name='vuehome'), # after login user will be redirect to this page
    url('^dashboard$', views.DashboardView.as_view(), name='dashboard'), # after login user will be redirect to this page
    url('^app-list/$', views.AppListView.as_view(), name='app_list'),
    url('^app/create/$', views.AppCreateView.as_view(), name='create_new_app'),
    #url('^create/$', views.DockerContainersView.as_view(), name='create_new'), # create docker containers using this
    url('^log/$', views.DockerUsageView.as_view(), name='usage_log'), # docker usage logs
    url('^build/(?P<id>[-\w]+)/$', views.DockerImageBuilder.as_view(), name='docker_image_builder'), # docker usage logs
    # # url('^create-organization/$', views.OrganizationCreateView.as_view(), name='create_organization'),
    # # url('^organization/(?P<id>[-\w]+)/update/$', views.OrganizationUpdateView.as_view(), name='update_organization'),
    # url('^organization/$', views.OrganizationView.as_view(), name='organization'), # organization details list view
    # url('^organization/(?P<id>[-\w]+)/update/$', views.OrganizationUpdateView.as_view(), name='update_organization'), # update organization details
    # url('^user-permission/(?P<id>[-\w]+)/update/$', views.UserPermissionUpdateView.as_view(), name='user_permission'), # working on it
    # url('^organization-users/$', views.OrganizationUserListView.as_view(), name='organization_users'), # registered userd inside the organization
    # url('^invoice/$', views.GenerateInvoiceView.as_view(), name='invoice'),  # start and stop docker container
    url('^docker/(?P<id>[-\w]+)/update/$', views.DockerContainersUpdateView.as_view(), name='update'), # start and stop docker container
    # # url('^permission/(?P<id>[-\w]+)/update/$', views.PermissionUpdateView.as_view(), name='update_permission'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
