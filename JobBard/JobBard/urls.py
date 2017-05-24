"""JobBard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from job_board.views import index, job_search, job_apply
from job_board.admin_views import admin_dashboard
from job_board.api import getApplicationFormInfo


urlpatterns = [
    url(r'^$', index),
    url(r'admin-dashboard/',admin_dashboard),
    url(r'job-search/',job_search),
    url(r'^admin/', admin.site.urls),
    url(r'^job-apply/(?P<jobID>[0-9]+)/$', job_apply),
    url(r'^api/jobform', getApplicationFormInfo),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
