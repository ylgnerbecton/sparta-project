#-*- coding: utf-8 -*-

##################################################
#               DJANGO IMPORTS                   #
##################################################
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404, render_to_response
from django.views.generic import RedirectView, View, UpdateView, ListView, DetailView, DeleteView
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
##################################################

##################################################
#               CUSTOM IMPORTS                   #
##################################################
from .models import ControleCusto, Divida, Parcela
from .forms import ControleCustoForm, DividaForm
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
class DividaRegister(JSONResponseMixin,View):
    def get(self, request):
        form = DividaForm
        return render(request, 'register.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = DividaForm(request.POST, request.FILES)
            
            nome_divida = request.POST['nome_divida']
            data_inicio = request.POST['data_inicio']
            data_atual = request.POST['data_atual']
            data_fim = request.POST['data_fim']
            id_parcela = request.POST['id_parcela']
            valor_parcela = request.POST['valor_parcela']
            valor_divida = request.POST['valor_divida']
            valor_pago = request.POST['valor_pago']

            if not nome_divida:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data_inicio:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not data_atual:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_atual = datetime.strptime(data_atual, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not data_fim:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_fim = datetime.strptime(data_fim, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not id_parcela:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_parcela:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_divida:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_pago:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                divida = Divida()
                divida.nome_divida = nome_divida
                divida.data_inicio = data_inicio
                divida.data_atual = data_atual
                divida.data_fim = data_fim
                divida.id_parcela = Parcela.objects.get(pk=parcela)
                divida.valor_parcela = valor_parcela
                divida.valor_divida = valor_divida
                divida.valor_pago = valor_pago
                divida.save()

                return redirect(reverse_lazy("divida-list"))

            else:
                form = DividaForm(request.POST)

        return render(request, 'default/divida/register.html', {'form': form, 'context':context})


class DividaEdit(JSONResponseMixin,View):
    def get(self, request, pk=None):
        divida = Divida.objects.get(pk=pk)
        id_parcela = Parcela.objects.get(pk=divida.id_parcela.pk)
        
        data_inicio = divida.data_inicio
        data_ini = ""
        if data_inicio:
            data_inicio = str(data_inicio).split("-")
            data_ini = data_inicio[2]+"/"+data_inicio[1]+"/"+data_inicio[0]

        data_atual = divida.data_atual
        data_atu = ""
        if data_atual:
            data_atual = str(data_atual).split("-")
            data_atu = data_atual[2]+"/"+data_atual[1]+"/"+data_atual[0]

        data_fim = divida.data_fim
        data_f = ""
        if data_fim:
            data_fim = str(data_fim).split("-")
            data_f = data_fim[2]+"/"+data_fim[1]+"/"+data_fim[0]

        form = DividaForm(
            initial={

            'nome_divida': divida.nome_divida,
            'data_inicio': divida.data_ini,
            'data_atual': divida.data_atu,
            'data_fim' : divida.data_f, 
            'parcela' : divida.id_parcela,
            'valor_parcela' : divida.valor_parcela,
            'valor_divida' : divida.valor_divida,
            'valor_pago' : divida.valor_pago,

           }
        )
        
        return render (request, 'default/divida/edit.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = DividaForm(request.POST, request.FILES)
            
            nome_divida = request.POST['nome_divida']
            data_inicio = request.POST['data_inicio']
            data_atual = request.POST['data_atual']
            data_fim = request.POST['data_fim']
            id_parcela = request.POST['id_parcela']
            valor_parcela = request.POST['valor_parcela']
            valor_divida = request.POST['valor_divida']
            valor_pago = request.POST['valor_pago']

            if not nome_divida:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data_inicio:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not data_atual:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_atual = datetime.strptime(data_atual, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not data_fim:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_fim = datetime.strptime(data_fim, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not id_parcela:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_parcela:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_divida:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_pago:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                divida = Divida()
                divida.nome_divida = nome_divida
                divida.data_inicio = data_inicio
                divida.data_atual = data_atual
                divida.data_fim = data_fim
                divida.id_parcela = Parcela.objects.get(pk=parcela)
                divida.valor_parcela = valor_parcela
                divida.valor_divida = valor_divida
                divida.valor_pago = valor_pago
                divida.save()

                return redirect(reverse_lazy("divida-list"))

            else:
                form = DividaForm(request.POST)

        return render(request, 'default/divida/register.html', {'form': form, 'context':context})


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