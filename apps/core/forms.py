#-*- coding: utf-8 -*-

##################################################
#               DJANGO IMPORTS                   #
##################################################
from django import forms
from django.conf import settings
from django.contrib.auth.forms import User, ReadOnlyPasswordHashField
from datetime import datetime
##################################################

##################################################
#               CUSTOM IMPORTS                   #
##################################################
from .models import ControleCusto, Despesa, Divida, ItensDesejados, Seguranca, Parcela, TipoConta, Renda
##################################################

'''
---------------------------------------
            ADMIN AREA
---------------------------------------
'''

class DespesaForm(forms.Form):
    tipodespesa = forms.CharField(max_length=45, required=False, label="Tipo de Despesa")
    
    def __init__(self, *args, **kwargs):
        super(DespesaForm, self).__init__(*args, **kwargs)
        
        # Tipo Despesa Fields widget
        self.fields['tipodespesa'].widget.attrs['class'] = 'form-control'
        self.fields['tipodespesa'].widget.attrs['placeholder'] = 'Digite o Tipo Despesa'

    pass

class DividaForm(forms.Form):
    nome_divida = forms.CharField(max_length=45, required=False, label="Nome da Divida")
    data_inicio = forms.DateField(required=False, label="Data Inicio")
    data_atual = forms.DateField(required=False, label="Data Atual")
    data_fim = forms.DateField(required=False, label="Data Fim")
    id_parcela = forms.ModelChoiceField('Parcela', required=False, widget=forms.Select, label="Parcelas do Produto")
    valor_parcela = forms.IntegerField(required=False, label="Valor Parcela")
    valor_divida = forms.IntegerField(required=False, label="Valor Divida")
    valor_pago = forms.IntegerField(required=False, label="Valor Pago")
    
    def __init__(self, *args, **kwargs):
        super(DividaForm, self).__init__(*args, **kwargs)
        
        # Nome Fields widget
        self.fields['nome_divida'].widget.attrs['class'] = 'form-control'
        self.fields['nome_divida'].widget.attrs['placeholder'] = ''

        # Parcela Fields widget
        self.fields['id_parcela'].widget.attrs['class'] = 'form-control'
        self.fields['id_parcela'].queryset = Parcela.objects.all()

        # Data Início Fields widget
        self.fields['data_atual'].widget.attrs['class'] = 'form-control'
        self.fields['data_atual'].widget.attrs['placeholder'] = ''

        # Data Início Fields widget
        self.fields['data_inicio'].widget.attrs['class'] = 'form-control'
        self.fields['data_inicio'].widget.attrs['placeholder'] = ''

        # Data Admissão Fields widget
        self.fields['data_fim'].widget.attrs['class'] = 'form-control'
        self.fields['data_fim'].widget.attrs['placeholder'] = ''

        # Valor Parcela Fields widget 
        self.fields['valor_parcela'].widget.attrs['class'] = 'form-control'
        self.fields['valor_parcela'].widget.attrs['placeholder'] = ''

        # Data divida Fields widget
        self.fields['valor_divida'].widget.attrs['class'] = 'form-control'
        self.fields['valor_divida'].widget.attrs['placeholder'] = ''

        # Valor Pago Fields widget 
        self.fields['valor_pago'].widget.attrs['class'] = 'form-control'
        self.fields['valor_pago'].widget.attrs['placeholder'] = ''

    pass

class ItensDesejadosForm(forms.Form):
    data_prevista = forms.DateField(required=False, label="Data Prevista de Compra")
    nome = forms.CharField(max_length=45, label="Nome do Item")
    valor = forms.IntegerField(required=False, label="Valor do Item")
    link = forms.URLField(required=False, label="Link")
    
    def __init__(self, *args, **kwargs):
        super(ItensDesejadosForm, self).__init__(*args, **kwargs)
        
        # Nome Fields widget
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['nome'].widget.attrs['placeholder'] = ''

        # Nome Fields widget
        self.fields['data_prevista'].widget.attrs['class'] = 'form-control'
        self.fields['data_prevista'].widget.attrs['placeholder'] = ''

        # Valor Fields widget
        self.fields['valor'].widget.attrs['class'] = 'form-control'
        self.fields['valor'].widget.attrs['placeholder'] = ''

        # Link Fields widget
        self.fields['link'].widget.attrs['class'] = 'form-control'
        self.fields['link'].widget.attrs['placeholder'] = ''

    pass

class TipoContaForm(forms.Form):
    tipoconta = forms.CharField(max_length=45, required=False, label="Tipo de Conta")

    def __init__(self, *args, **kwargs):
        super(TipoContaForm, self).__init__(*args, **kwargs)
        
        # Tipo de Conta Fields widget
        self.fields['tipoconta'].widget.attrs['class'] = 'form-control'
        self.fields['tipoconta'].widget.attrs['placeholder'] = 'Digite o Tipo de Conta'

    pass

class SegurancaForm(forms.Form):
    id_tipoconta = forms.ModelChoiceField('TipoConta', required=False, widget=forms.Select, label="Tipo de Conta")
    email = forms.CharField(max_length=45, label="E-mail")
    senha = forms.CharField(max_length=45, required=False, label="Senha")
    
    def __init__(self, *args, **kwargs):
        super(SegurancaForm, self).__init__(*args, **kwargs)

        # Tipo Conta Fields widget
        self.fields['id_tipoconta'].widget.attrs['class'] = 'form-control'
        self.fields['id_tipoconta'].queryset = TipoConta.objects.all()

        # E-mail Fields widget
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = ''

        # Senha Fields widget
        self.fields['senha'].widget.attrs['class'] = 'form-control'
        self.fields['senha'].widget.attrs['placeholder'] = ''

    pass
    
class ControleCustoForm(forms.Form):
    nome = forms.CharField(max_length=45, label="Nome")
    data = forms.DateTimeField(required=False, label="Data")
    id_renda = forms.ModelChoiceField('Renda', required=False, widget=forms.Select, label="Tipo de Renda")
    valor_ganho_renda = forms.IntegerField(required=False, label="Valor Ganho")
    id_despesa = forms.ModelChoiceField('Despesa', required=False, widget=forms.Select, label="Tipo de Despesa")
    valor_anterior_despesa = forms.IntegerField(required=False, label="Valor Anterior")
    valor_retirado_despesa = forms.IntegerField(required=False, label="Valor Retirado")
    valor_atual_despesa = forms.IntegerField(required=False, label="Valor Atual")
    comentario = forms.CharField(max_length=1000, required=False, label="Comentário")

    def __init__(self, *args, **kwargs):
        super(ControleCustoForm, self).__init__(*args, **kwargs)
        
        # Nome Fields widget
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['nome'].widget.attrs['placeholder'] = ''

        # Data Fields widget
        self.fields['data'].widget.attrs['class'] = 'form-control'
        self.fields['data'].widget.attrs['placeholder'] = ''

        # Tipo de Renda Fields widget
        self.fields['id_renda'].widget.attrs['class'] = 'form-control'
        self.fields['id_renda'].queryset = Renda.objects.all()

        # Valor Ganho Fields widget
        self.fields['valor_ganho_renda'].widget.attrs['class'] = 'form-control'
        self.fields['valor_ganho_renda'].widget.attrs['placeholder'] = ''

        # Despesa Fields widget
        self.fields['id_despesa'].widget.attrs['class'] = 'form-control'
        self.fields['id_despesa'].queryset = Despesa.objects.all()

        # Valor Anterior Fields widget
        self.fields['valor_anterior_despesa'].widget.attrs['class'] = 'form-control'
        self.fields['valor_anterior_despesa'].widget.attrs['placeholder'] = ''

        # Valor Retirado Fields widget
        self.fields['valor_retirado_despesa'].widget.attrs['class'] = 'form-control'
        self.fields['valor_retirado_despesa'].widget.attrs['placeholder'] = ''

        # Valor Atual Fields widget 
        self.fields['valor_atual_despesa'].widget.attrs['class'] = 'form-control'
        self.fields['valor_atual_despesa'].widget.attrs['placeholder'] = ''

        # Comentario Fields widget 
        self.fields['comentario'].widget.attrs['class'] = 'form-control'
        self.fields['comentario'].widget.attrs['placeholder'] = ''

    pass