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
from .views import ControleCustoRegister, ControleCustoList, ControleCustoDetail, ControleCustoEdit, ControleCustoDelete
from .views import ItensDesejadosRegister, ItensDesejadosList, ItensDesejadosDetail, ItensDesejadosEdit, ItensDesejadosDelete
from .views import SegurancaRegister, SegurancaList, SegurancaEdit, SegurancaDetail, SegurancaDelete
##################################################

urlpatterns = [
	url(r'^/$', ControleCustoList.as_view(), name="home"),
    url(r'^divida/register/$', DividaRegister.as_view(), name="divida-register"),
	url(r'^divida/list/$', DividaList.as_view(), name="divida-list"),
	url(r'^divida/detail/(?P<pk>\d+)/$', DividaDetail.as_view(), name="divida-detail"),
	url(r'^divida/edit/(?P<pk>\d+)/$', DividaEdit.as_view(), name="divida-edit"),
	url(r'^divida/delete/(?P<pk>\d+)/$', DividaDelete.as_view(), name="divida-delete"),

	url(r'^seguranca/register/$', SegurancaRegister.as_view(), name="seguranca-register"),
	url(r'^seguranca/list/$', SegurancaList.as_view(), name="seguranca-list"),
	url(r'^seguranca/detail/(?P<pk>\d+)/$', SegurancaDetail.as_view(), name="seguranca-detail"),
	url(r'^seguranca/edit/(?P<pk>\d+)/$', SegurancaEdit.as_view(), name="seguranca-edit"),
	url(r'^seguranca/delete/(?P<pk>\d+)/$', SegurancaDelete.as_view(), name="seguranca-delete"),

	url(r'^itensdesejados/register/$', ItensDesejadosRegister.as_view(), name="itensdesejados-register"),
	url(r'^itensdesejados/list/$', ItensDesejadosList.as_view(), name="itensdesejados-list"),
	url(r'^itensdesejados/detail/(?P<pk>\d+)/$', ItensDesejadosDetail.as_view(), name="itensdesejados-detail"),
	url(r'^itensdesejados/edit/(?P<pk>\d+)/$', ItensDesejadosEdit.as_view(), name="itensdesejados-edit"),
	url(r'^itensdesejados/delete/(?P<pk>\d+)/$', ItensDesejadosDelete.as_view(), name="itensdesejados-delete"),

	url(r'^controlecusto/register/$', ControleCustoRegister.as_view(), name="controlecusto-register"),
	url(r'^controlecusto/list/$', ControleCustoList.as_view(), name="controlecusto-list"),
	url(r'^controlecusto/detail/(?P<pk>\d+)/$', ControleCustoDetail.as_view(), name="controlecusto-detail"),
	url(r'^controlecusto/edit/(?P<pk>\d+)/$', ControleCustoEdit.as_view(), name="controlecusto-edit"),
	url(r'^controlecusto/delete/(?P<pk>\d+)/$', ControleCustoDelete.as_view(), name="controlecusto-delete"),
]