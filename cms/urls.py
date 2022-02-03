from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from cms import views

app_name = 'cms'

urlpatterns = [
    url('^home$', views.Homepage.as_view(), name='home'),
    url('^$', views.LandingPage.as_view(), name='index'),
    url('^accounts/login/$', views.LoginViewTest.as_view(), name='login'),
    # url('^dashboard$', views.DashboardView.as_view(), name='dashboard'),
    # url('^create/$', views.DockerContainersView.as_view(), name='create_new'),
    # url('^log/$', views.DockerUsageView.as_view(), name='usage_log'),
    # url('^docker/(?P<id>[-\w]+)/update/$', views.DockerContainersUpdateView.as_view(), name='update'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)