#-*- coding: utf-8 -*-

##################################################
#               DJANGO IMPORTS                   #
##################################################
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404, render_to_response
from django.views.generic import RedirectView, View, UpdateView, ListView, DetailView, DeleteView, CreateView
from django.contrib.auth import authenticate, login, logout as django_logout
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse)
from django.forms import formset_factory
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Count, Avg, Max, Min, Sum
from datetime import datetime
##################################################

##################################################
#               CUSTOM IMPORTS                   #
##################################################
from .models import ControleCusto, Divida, Parcela, ControleCusto, Renda, Despesa, Seguranca, TipoConta, ItensDesejados
from .forms import ControleCustoForm, DividaForm, ControleCustoForm, SegurancaForm, ItensDesejadosForm
##################################################
'''
    CONVERT TO JSON
'''
class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

'''
----------------------------------------
            DIVIDA METHODS
----------------------------------------
'''
class DividaRegister(JSONResponseMixin,CreateView):
    model = Divida
    fields = ('__all__')
    template_name = 'default/divida/register.html'
    success_url = reverse_lazy("divida-list")

    def get(self, request):
        form = DividaForm
        return render(request, 'default/divida/register.html', {'form':form})


class DividaEdit(JSONResponseMixin,UpdateView):
    model = Divida
    fields = ('__all__')
    template_name = 'default/divida/edit.html'
    success_url = reverse_lazy("divida-list")

    def get(self, request, pk=None):
        divida = Divida.objects.get(pk=pk)

        form = DividaForm(
            initial={

            'nome_divida': divida.nome_divida,
            'data_inicio': divida.data_inicio,
            'data_atual': divida.data_fim,
            'data_fim' : divida.data_fim, 
            'parcela' : divida.id_parcela,
            'valor_parcela' : divida.valor_parcela,
            'valor_divida' : divida.valor_divida,
            'valor_pago' : divida.valor_pago,

           }
        )
        
        return render (request, 'default/divida/edit.html', {'form':form})


class DividaList(JSONResponseMixin,ListView):
    model = Divida
    template_name = 'default/divida/list.html'

    def get_context_data(self, **kwargs):
        context = super(DividaList, self).get_context_data(**kwargs)
        return context


class DividaDetail(JSONResponseMixin,DetailView):
    model = Divida
    template_name = 'default/divida/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DividaDetail, self).get_context_data(**kwargs)
        return context


class DividaDelete(JSONResponseMixin,DeleteView):
    model = Divida
    success_url = reverse_lazy('divida-list')
    template_name = 'default/divida/delete.html'

'''
----------------------------------------
            CONTROLE DE CUSTO METHODS
----------------------------------------
'''
class ControleCustoRegister(JSONResponseMixin,CreateView):
    model = ControleCusto
    fields = ('__all__')
    template_name = 'default/controle-custo/register.html'
    success_url = reverse_lazy("controlecusto-list")

    def get(self, request):
        form = ControleCustoForm
        return render(request, 'default/controle-custo/register.html', {'form':form})


class ControleCustoEdit(JSONResponseMixin,UpdateView):
    model = ControleCusto
    fields = ('__all__')
    template_name = 'default/controle-custo/edit.html'
    success_url = reverse_lazy("controlecusto-list")

    def get(self, request, pk=None):
        controlecusto = ControleCusto.objects.get(pk=pk)

        form = ControleCustoForm(
            initial={

            'nome': controlecusto.nome,
            'data': controlecusto.data,
            'id_renda': controlecusto.id_renda,
            'valor_ganho_renda' : controlecusto.valor_ganho_renda, 
            'id_despesa' : controlecusto.id_despesa,
            'valor_anterior_despesa' : controlecusto.valor_anterior_despesa,
            'valor_retirado_despesa' : controlecusto.valor_retirado_despesa,
            'valor_atual_despesa' : controlecusto.valor_atual_despesa,
            'comentario' : controlecusto.comentario,

           }
        )
        
        return render(request, 'default/controle-custo/edit.html', {'form':form})


class ControleCustoList(JSONResponseMixin,ListView):
    model = ControleCusto
    template_name = 'default/controle-custo/list.html'

    def get_context_data(self, **kwargs):
        context = super(ControleCustoList, self).get_context_data(**kwargs)
        return context


class ControleCustoDetail(JSONResponseMixin,DetailView):
    model = ControleCusto
    template_name = 'default/controle-custo/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ControleCustoDetail, self).get_context_data(**kwargs)
        return context


class ControleCustoDelete(JSONResponseMixin,DeleteView):
    model = ControleCusto
    success_url = reverse_lazy('controlecusto-list')
    template_name = 'default/controle-custo/delete.html'

'''
----------------------------------------
            DIVIDA METHODS
----------------------------------------
'''
class SegurancaRegister(JSONResponseMixin,CreateView):
    model = Seguranca
    fields = ('__all__')
    template_name = 'default/seguranca/register.html'
    success_url = reverse_lazy("seguranca-list")

    def get(self, request):
        form = SegurancaForm
        return render(request, 'default/seguranca/register.html', {'form':form})


class SegurancaEdit(JSONResponseMixin,UpdateView):
    model = Seguranca
    fields = ('__all__')
    template_name = 'default/seguranca/edit.html'
    success_url = reverse_lazy("seguranca-list")

    def get(self, request, pk=None):
        seguranca = Seguranca.objects.get(pk=pk)

        form = DividaForm(
            initial={

            'email': seguranca.email,
            'senha': seguranca.senha,
            'id_tipoconta': seguranca.id_tipoconta,

           }
        )
        
        return render (request, 'default/seguranca/edit.html', {'form':form})


class SegurancaList(JSONResponseMixin,ListView):
    model = Seguranca
    template_name = 'default/seguranca/list.html'

    def get_context_data(self, **kwargs):
        context = super(SegurancaList, self).get_context_data(**kwargs)
        return context


class SegurancaDetail(JSONResponseMixin,DetailView):
    model = Seguranca
    template_name = 'default/seguranca/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SegurancaDetail, self).get_context_data(**kwargs)
        return context


class SegurancaDelete(JSONResponseMixin,DeleteView):
    model = Seguranca
    success_url = reverse_lazy('seguranca-list')
    template_name = 'default/seguranca/delete.html'

'''
----------------------------------------
            DIVIDA METHODS
----------------------------------------
'''
class ItensDesejadosRegister(JSONResponseMixin,CreateView):
    model = ItensDesejados
    fields = ('__all__')
    template_name = 'default/itensdesejados/register.html'
    success_url = reverse_lazy("itensdesejados-list")

    def get(self, request):
        form = ItensDesejadosForm
        return render(request, 'default/itensdesejados/register.html', {'form':form})


class ItensDesejadosEdit(JSONResponseMixin,UpdateView):
    model = ItensDesejados
    fields = ('__all__')
    template_name = 'default/itensdesejados/edit.html'
    success_url = reverse_lazy("itensdesejados-list")

    def get(self, request, pk=None):
        itensdesejados = ItensDesejados.objects.get(pk=pk)

        form = DividaForm(
            initial={

            'nome': itensdesejados.nome,
            'data_prevista': itensdesejados.data_prevista,
            'imagem_produto': itensdesejados.imagem_produto,
            'link' : itensdesejados.link, 
            'valor' : itensdesejados.valor, 

           }
        )
        
        return render (request, 'default/itensdesejados/edit.html', {'form':form})


class ItensDesejadosList(JSONResponseMixin,ListView):
    model = ItensDesejados
    template_name = 'default/itensdesejados/list.html'

    def get_context_data(self, **kwargs):
        context = super(ItensDesejadosList, self).get_context_data(**kwargs)
        return context


class ItensDesejadosDetail(JSONResponseMixin,DetailView):
    model = ItensDesejados
    template_name = 'default/itensdesejados/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ItensDesejadosDetail, self).get_context_data(**kwargs)
        return context


class ItensDesejadosDelete(JSONResponseMixin,DeleteView):
    model = ItensDesejados
    success_url = reverse_lazy('itensdesejados-list')
    template_name = 'default/itensdesejados/delete.html'