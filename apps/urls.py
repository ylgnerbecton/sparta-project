#-*- coding: utf-8 -*-

##################################################
#               DJANGO IMPORTS                   #
##################################################
from django.conf.urls import include, url, patterns
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import views
##################################################

##################################################
#               CUSTOM IMPORTS                   #
##################################################
from .views import DividaRegister, DividaList, DividaDetail, DividaEdit, DividaDelete
##################################################

urlpatterns = [
    url(r'^divida/register/$', DividaRegister.as_view(), name="divida-register"),
	url(r'^divida/list/$', DividaList.as_view(), name="divida-list"),
	url(r'^divida/detail/(?P<pk>\d+)/$', DividaDetail.as_view(), name="divida-detail"),
	url(r'^divida/edit/(?P<pk>\d+)/$', DividaEdit.as_view(), name="divida-edit"),
	url(r'^divida/delete/(?P<pk>\d+)/$', DividaDelete.as_view(), name="divida-delete"),
]