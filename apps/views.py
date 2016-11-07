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
class DividaRegister(JSONResponseMixin,View):
    def get(self, request):
        form = DividaForm
        return render(request, 'default/divida/register.html', {'form':form})

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
                divida.id_parcela = Parcela.objects.get(pk=id_parcela)
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

    def post(self, request, pk=None, *args, **kwargs):
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
                divida.id_parcela = Parcela.objects.get(pk=id_parcela)
                divida.valor_parcela = valor_parcela
                divida.valor_divida = valor_divida
                divida.valor_pago = valor_pago
                divida.save()

                return redirect(reverse_lazy("divida-list"))

            else:
                form = DividaForm(request.POST)

        return render(request, 'default/divida/edit.html', {'form': form, 'context':context})


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
class ControleCustoRegister(JSONResponseMixin,View):
    def get(self, request):
        form = ControleCustoForm
        return render(request, 'default/controle-custo/register.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = ControleCustoForm(request.POST, request.FILES)
            
            nome = request.POST['nome']
            data = request.POST['data']
            id_renda = request.POST['id_renda']
            valor_ganho_renda = request.POST['valor_ganho_renda']
            id_despesa = request.POST['id_despesa']
            valor_anterior_despesa = request.POST['valor_anterior_despesa']
            valor_retirado_despesa = request.POST['valor_retirado_despesa']
            valor_atual_despesa = request.POST['valor_atual_despesa']
            comentario = request.POST['comentario']

            if not nome:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not id_renda:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_ganho_renda:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not id_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_anterior_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_retirado_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_atual_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not comentario:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                controlecusto = ControleCusto()
                controlecusto.nome = nome
                controlecusto.data = data
                controlecusto.id_renda = Renda.objects.get(pk=id_renda)
                controlecusto.valor_ganho_renda = valor_ganho_renda
                controlecusto.id_despesa = Despesa.objects.get(pk=id_despesa)
                controlecusto.valor_anterior_despesa = valor_anterior_despesa
                controlecusto.valor_retirado_despesa = valor_retirado_despesa
                controlecusto.valor_atual_despesa = valor_atual_despesa
                controlecusto.comentario = comentario
                controlecusto.save()

                return redirect(reverse_lazy("controlecusto-list"))

            else:
                form = ControleCustoForm(request.POST)

        return render(request, 'default/controle-custo/register.html', {'form': form, 'context':context})


class ControleCustoEdit(JSONResponseMixin,View):
    def get(self, request, pk=None):
        controlecusto = ControleCusto.objects.get(pk=pk)
        id_renda = Renda.objects.get(pk=controlecusto.id_renda.pk)
        id_despesa = Despesa.objects.get(pk=controlecusto.id_despesa.pk)

        data = controlecusto.data
        dated = ""
        if data:
            data = str(data).split("-")
            dated = data[2]+"/"+data[1]+"/"+data[0]

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
        
        return render (request, 'default/controle-custo/edit.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = ControleCustoForm(request.POST, request.FILES)
            
            nome = request.POST['nome']
            data = request.POST['data']
            id_renda = request.POST['id_renda']
            valor_ganho_renda = request.POST['valor_ganho_renda']
            id_despesa = request.POST['id_despesa']
            valor_anterior_despesa = request.POST['valor_anterior_despesa']
            valor_retirado_despesa = request.POST['valor_retirado_despesa']
            valor_atual_despesa = request.POST['valor_atual_despesa']
            comentario = request.POST['comentario']

            if not nome:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not id_renda:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_ganho_renda:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not id_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_anterior_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_retirado_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor_atual_despesa:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not comentario:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                controlecusto = ControleCusto()
                controlecusto.nome = nome
                controlecusto.data = data
                controlecusto.id_renda = Renda.objects.get(pk=id_renda)
                controlecusto.valor_ganho_renda = valor_ganho_renda
                controlecusto.id_despesa = Despesa.objects.get(pk=id_despesa)
                controlecusto.valor_anterior_despesa = valor_anterior_despesa
                controlecusto.valor_retirado_despesa = valor_retirado_despesa
                controlecusto.valor_atual_despesa = valor_atual_despesa
                controlecusto.comentario = comentario
                controlecusto.save()

                return redirect(reverse_lazy("controlecusto-list"))

            else:
                form = ControleCustoForm(request.POST)

        return render(request, 'default/controle-custo/edit.html', {'form': form, 'context':context})


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
class SegurancaRegister(JSONResponseMixin,View):
    def get(self, request):
        form = SegurancaForm
        return render(request, 'default/seguranca/register.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = SegurancaForm(request.POST, request.FILES)
            
            id_tipoconta = request.POST['id_tipoconta']
            email = request.POST['email']
            senha = request.POST['senha']

            if not id_tipoconta:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not email:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not senha:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                seguranca = Seguranca()
                seguranca.email = email
                seguranca.senha = senha
                seguranca.id_tipoconta = TipoConta.objects.get(pk=id_tipoconta)
                seguranca.save()

                return redirect(reverse_lazy("seguranca-list"))

            else:
                form = SegurancaForm(request.POST)

        return render(request, 'default/seguranca/register.html', {'form': form, 'context':context})


class SegurancaEdit(JSONResponseMixin,View):
    def get(self, request, pk=None):
        seguranca = Seguranca.objects.get(pk=pk)
        id_tipoconta = TipoConta.objects.get(pk=id_tipoconta.pk)

        form = DividaForm(
            initial={

            'email': seguranca.email,
            'senha': seguranca.senha,
            'id_tipoconta': seguranca.id_tipoconta,

           }
        )
        
        return render (request, 'default/seguranca/edit.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = SegurancaForm(request.POST, request.FILES)
            
            id_tipoconta = request.POST['id_tipoconta']
            email = request.POST['email']
            senha = request.POST['senha']

            if not id_tipoconta:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not email:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not senha:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                seguranca = Seguranca()
                seguranca.email = email
                seguranca.senha = senha
                seguranca.id_tipoconta = TipoConta.objects.get(pk=id_tipoconta)
                seguranca.save()

                return redirect(reverse_lazy("seguranca-list"))

            else:
                form = SegurancaForm(request.POST)

        return render(request, 'default/seguranca/edit.html', {'form': form, 'context':context})


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
class ItensDesejadosRegister(JSONResponseMixin,View):
    def get(self, request):
        form = ItensDesejadosForm
        return render(request, 'default/itensdesejados/register.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = ItensDesejadosForm(request.POST, request.FILES)
            
            data_prevista = request.POST['data_prevista']
            nome = request.POST['nome']
            valor = request.POST['valor']
            imagem_produto = request.POST['imagem_produto']
            link = request.POST['link']

            if not nome:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data_prevista:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_prevista = datetime.strptime(data_prevista, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not imagem_produto:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not valor:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not link:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                itensdesejados = ItensDesejados()
                itensdesejados.nome = nome
                itensdesejados.data_prevista = data_prevista
                itensdesejados.imagem_produto = imagem_produto
                itensdesejados.link = link
                itensdesejados.valor = valor
                itensdesejados.save()

                return redirect(reverse_lazy("itensdesejados-list"))

            else:
                form = ItensDesejadosForm(request.POST)

        return render(request, 'default/itensdesejados/register.html', {'form': form, 'context':context})


class ItensDesejadosEdit(JSONResponseMixin,View):
    def get(self, request, pk=None):
        itensdesejados = ItensDesejados.objects.get(pk=pk)
        
        data_prevista = itensdesejados.data_prevista
        data_previ = ""
        if data_prevista:
            data_prevista = str(data_prevista).split("-")
            data_previ = data_prevista[2]+"/"+data_prevista[1]+"/"+data_prevista[0]

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

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':            
            form = ItensDesejadosForm(request.POST, request.FILES)
            
            data_prevista = request.POST['data_prevista']
            nome = request.POST['nome']
            imagem_produto = request.POST['imagem_produto']
            link = request.POST['link']
            valor = request.POST['valor']

            if not valor:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not nome:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not data_prevista:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'
            else:
                data_prevista = datetime.strptime(data_prevista, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not imagem_produto:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not link:
                context['error_msg'] = 'Por favor, preencha o campo corretamente !'

            if not context:

                itensdesejados = ItensDesejados()
                itensdesejados.nome = nome
                itensdesejados.data_prevista = data_prevista
                itensdesejados.imagem_produto = imagem_produto
                itensdesejados.link = link
                itensdesejados.valor = valor
                itensdesejados.save()

                return redirect(reverse_lazy("itensdesejados-list"))

            else:
                form = ItensDesejadosForm(request.POST)

        return render(request, 'default/itensdesejados/edit.html', {'form': form, 'context':context})


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