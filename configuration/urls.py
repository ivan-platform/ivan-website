"""configuration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls.conf import include

from mainapp import views
from configuration import views as frontend_views

app_name = 'mainapp'

vue_urls = [
    path('', frontend_views.frontend),
    # path('vue/', frontend_views.frontend),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuehome/', include(vue_urls)),
    url('', include('mainapp.urls'), name='home'),
    url('^accounts/register/$', views.RegisterView.as_view(), name='register'),
    url('^accounts/login/$', views.LoginView.as_view(), name='login'),
    url('^accounts/logout/$', auth_views.LogoutView.as_view(),name='logout'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
