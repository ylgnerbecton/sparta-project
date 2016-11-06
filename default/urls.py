
#-*- coding: utf-8 -*-

##################################################
#				DJANGO IMPORTS                   #
##################################################
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
##################################################

##################################################
#				CUSTOM IMPORTS                   #
##################################################
from .views import Register, Login, Logout # AUTH VIEWS
from .views import Dashboard # DASHBOARD VIEW
from .views import Profile # PROFILE VIEW
from .views import UserRegister, UserList, UserDetail, UserEdit, UserDelete # USER VIEWS
from .views import CompanyRegister, CompanyList, CompanyDetail, CompanyEdit, CompanyDelete # COMPANY VIEWS
from .views import get_cnpj_json, get_cep_json # SERVICES
##################################################


urlpatterns = (
	url(r'^auth/login/$', Login.as_view(), name="login"),
	url(r'^auth/register/$', Register.as_view(), name="register"),
	url(r'^auth/logout/$', login_required(Logout.as_view()), name="logout"),
	url(r'^dashboard/home/$', login_required(Dashboard.as_view()), name="home"),
	url(r'^dashboard/profile/$', login_required(Profile.as_view()), name="profile"),
	url(r'^dashboard/user/register/$', login_required(UserRegister.as_view()), name="user-register"),
	url(r'^dashboard/user/list/$', login_required(UserList.as_view()), name="user-list"),
	url(r'^dashboard/user/detail/(?P<pk>\d+)/$', login_required(UserDetail.as_view()), name="user-detail"),
	url(r'^dashboard/user/edit/(?P<pk>\d+)/$', login_required(UserEdit.as_view()), name="user-edit"),
	url(r'^dashboard/user/delete/(?P<pk>\d+)/$', login_required(UserDelete.as_view()), name="user-delete"),
	url(r'^dashboard/company/register/$', login_required(CompanyRegister.as_view()), name="company-register"),
	url(r'^dashboard/company/list/$', login_required(CompanyList.as_view()), name="company-list"),
	url(r'^dashboard/company/detail/(?P<pk>\d+)/$', login_required(CompanyDetail.as_view()), name="company-detail"),
	url(r'^dashboard/company/edit/(?P<pk>\d+)/$', login_required(CompanyEdit.as_view()), name="company-edit"),
	url(r'^dashboard/company/delete/(?P<pk>\d+)/$', login_required(CompanyDelete.as_view()), name="company-delete"),
	url(r'^service/cnpj/', login_required(get_cnpj_json), name="service-cnpj"),
	url(r'^service/cep/', login_required(get_cep_json), name="service-cep"),
)