from django.contrib import admin

# Register your models here.
from .models import Renda, Despesa, Divida, ControleCusto, Parcela, Seguranca, ItensDesejados, TipoConta

admin.site.register(Renda)
admin.site.register(Despesa)
admin.site.register(Divida)
admin.site.register(ControleCusto)
admin.site.register(Parcela)
admin.site.register(Seguranca)
admin.site.register(ItensDesejados)
admin.site.register(TipoConta)