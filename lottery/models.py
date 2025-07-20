from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Dollar(models.Model):
    exchange_rate = models.FloatField(_("Tasa de cambio"))
    history = HistoricalRecords()
    updated = models.DateTimeField(_("Última modificación"), auto_now=True)

    def __str__(self):
        return f'{self.exchange_rate}'


class Lottery(models.Model):
    description = models.CharField(_("Descripción"), max_length=200)
    image = models.ImageField(_("Imagen"), upload_to='images/')
    price = models.FloatField(_("Precio"))
    closing_date = models.DateField(_("Fecha de cierre"))
    closed = models.BooleanField(_("Cerrada"))


    class Meta:
        verbose_name = _("lottery")
        verbose_name_plural = _("lotteries")

    def __str__(self):
        return self.description
    

class Order(models.Model):
    STATUS = [
        (0, 'Por confimar'),
        (1, 'Confirmada'),
        (2, 'Rechazada'),
    ]

    lottery = models.ForeignKey("lottery.Lottery", verbose_name=_("Sorteo"), on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.CustomUser", verbose_name=_("Usuario"), on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(_("Cantidad"))
    status = models.IntegerField(_("Status"), choices=STATUS, default=0)
    reference = models.IntegerField(_("Referencia"), blank=True, null=True)
    dollar = models.ForeignKey("lottery.Dollar", verbose_name=_("Tasa del dolar"), on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)


