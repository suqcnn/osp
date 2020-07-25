"""osp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include

import api.views
import api.views.cluster
import api.views.user

urlpatterns = [
    re_path('^/?$', api.views.index),
    re_path('^ui/login/admin/?$', api.views.ui_login_admin),
    re_path('^ui/login/?$', api.views.ui_login),
    re_path('^ui/.*?$', api.views.ui),
    re_path('health/?', api.views.health),
    re_path('osp/api/login/?', api.views.user.login),
    re_path('osp/api/logout/?', api.views.user.logout),
    re_path('osp/api/has_admin/?', api.views.user.has_admin),
    re_path('osp/api/cluster/agent/?', api.views.cluster.agent),
    path('osp/api/', include('api.urls')),
]

urlpatterns += staticfiles_urlpatterns()
