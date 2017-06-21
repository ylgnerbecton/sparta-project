from django.db import models
from datetime import datetime
# Create your models here.

class Renda(models.Model):
    id_renda = models.AutoField(primary_key=True)
    tiporenda = models.CharField(max_length=45, null=False, blank=False, verbose_name="Tipo de Renda")
    def __str__(self):
        return self.tiporenda
		
class Despesa(models.Model):
	id_despesa = models.AutoField(primary_key=True)
	tipodespesa = models.CharField(max_length=45, null=True, blank=True, verbose_name="Tipo de Despesa")
	def __str__(self):
		return self.tipodespesa

class Divida(models.Model):
	id_divida = models.AutoField(primary_key=True)
	nome_divida = models.CharField(max_length=45, null=False, blank=False, verbose_name="Nome da Divida")
	data_inicio = models.DateField(default=datetime.now, null=True, blank=True, verbose_name="Data Inicio")
	data_atual = models.DateField(default=datetime.now, null=True, blank=True, verbose_name="Data Atual")
	data_fim = models.DateField(default=datetime.now, null=True, blank=True, verbose_name="Data Fim")
	id_parcela = models.ForeignKey('Parcela', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Parcelas do Produto")
	valor_parcela = models.IntegerField(null=True, blank=True, verbose_name="Valor Parcela")
	valor_divida = models.IntegerField(null=True, blank=True, verbose_name="Valor Divida")
	valor_pago = models.IntegerField(null=True, blank=True, verbose_name="Valor Pago")
	def __str__(self):
		return self.nome_divida

class Parcela(models.Model):
	id_parcela = models.AutoField(primary_key=True)
	parcela = models.CharField(max_length=45, null=True, blank=True, verbose_name="Parcelas")
	def __str__(self):
		return self.parcela

class ItensDesejados(models.Model):
	id_itemdesejado = models.AutoField(primary_key=True)
	data_prevista = models.DateField(default=datetime.now, null=True, blank=True, verbose_name="Data Prevista de Compra")
	nome = models.CharField(max_length=45, null=False, blank=False, verbose_name="Nome do Item")
	imagem_produto = models.ImageField(upload_to="default/users",null=True, blank=True)
	valor = models.IntegerField(null=True, blank=True, verbose_name="Valor do Item")
	link = models.URLField(null=True, blank=True, verbose_name="Link")
	def __str__(self):
		return self.nome

class TipoConta(models.Model):
	id_tipoconta = models.AutoField(primary_key=True)
	tipoconta = models.CharField(max_length=45, null=True, blank=True, verbose_name="Tipo de Conta")
	def __str__(self):
		return self.tipoconta

class Seguranca(models.Model):
	id_seguranca = models.AutoField(primary_key=True)
	id_tipoconta = models.ForeignKey('TipoConta', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Tipo de Conta")
	email = models.CharField(max_length=45, null=False, blank=False, verbose_name="E-mail")
	senha = models.CharField(max_length=45, null=True, blank=True, verbose_name="Senha")
	def __str__(self):
		return self.email
	
class ControleCusto(models.Model):
	id_controlecusto = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=45, null=False, blank=False, verbose_name="Nome")
	data = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name="Data")
	id_renda = models.ForeignKey('Renda', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Tipo de Renda")
	valor_ganho_renda = models.IntegerField(null=True, blank=True, verbose_name="Valor Ganho")
	id_despesa = models.ForeignKey('Despesa', null=True, blank=True, on_delete=models.DO_NOTHING , verbose_name="Tipo de Despesa")
	valor_anterior_despesa = models.IntegerField(null=True, blank=True, verbose_name="Valor Anterior")
	valor_retirado_despesa = models.IntegerField(null=True, blank=True, verbose_name="Valor Retirado")
	valor_atual_despesa = models.IntegerField(null=True, blank=True, verbose_name="Valor Atual")
	comentario = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Comentário")
	def __str__(self):
		return self.nome