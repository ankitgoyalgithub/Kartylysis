"""PylysisProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
# from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from SMS import views
#from django.contrib import admin
from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register(r'Templates',views.TemplateViewSet)
router.register(r'Messages',views.MessagesViewSet)
router.register(r'Clients',views.ClientViewSet)
router.register(r'Admin',views.AdminViewSet)


urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^validateClient/$', views.validateClient),
    url(r'^validateAdmin/$', views.validateAdmin),
    url(r'^addNewTemplate/$', views.addNewTemplate),
    url(r'^deleteTemplate/$', views.deleteTemplate),
    url(r'^updateTemplate/$', views.updateTemplate),
    url(r'^getUserMessages/$', views.getUserMessages),
    url(r'^uploadCSV/$', views.uploadClientCSVData),
    url(r'^updateClient/$', views.updateClient),
    url(r'^getTemplateMessages/$', views.getTemplateMessages),
    url(r'^exportMessageToCSV/$', views.exportMessageToCSV),
    url(r'^exportMessageToCSVWithFilters/$', views.exportMessageToCSVWithFilter),
    url(r'^getRegisteredCount/$', views.getResteredUserCount)

]
urlpatterns += router.urls
