from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
import random




class Dollar(models.Model):
    exchange_rate = models.FloatField(_("Tasa de cambio"))
    history = HistoricalRecords()
    updated = models.DateTimeField(_("Última modificación"), auto_now=True)

    def __str__(self):
        return f'{self.exchange_rate}'


class Lottery(models.Model):
    AVAILABLE_TICKETS = 10000
    description = models.TextField(_("Descripción"))
    image = models.ImageField(_("Imagen"), upload_to='images/')
    price = models.FloatField(_("Precio"))
    closing_date = models.DateField(_("Fecha de cierre"))
    closed = models.BooleanField(_("Cerrada"))
    
    history = HistoricalRecords()
    created = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    updated = models.DateTimeField(_("Última modificación"), auto_now=True)

    class Meta:
        verbose_name = _("lottery")
        verbose_name_plural = _("lotteries")

    def __str__(self):
        return self.description
    

class Order(models.Model):
    phone_validator = RegexValidator(
        regex=r'^04\d{9}$',
        message="Ingrese un nro. de teléfono válido. ej. 04123456789"
    )
    
    PAYMENT_METHOD = [
        (0, 'Pago móvil'),
        (1, 'Zelle'),
        (2, 'Paypal'),
    ]
    TYPE_OF_DNI = [
        (0, 'V'),
        (1, 'E'),
        (2, 'J'),
    ]
    BANK_CODE = [
        ("0102","BANCO DE VENEZUELA"),
        ("0104","BANCO VENEZOLANO DE CREDITO"),
        ("0105","BANCO MERCANTIL"),
        ("0108","BBVA PROVINCIAL"),
        ("0114","BANCARIBE"),
        ("0115","BANCO EXTERIOR"),
        ("0128","BANCO CARONI"),
        ("0134","BANESCO"),
        ("0137","BANCO SOFITASA"),
        ("0138","BANCO PLAZA"),
        ("0146","BANGENTE"),
        ("0151","BANCO FONDO COMUN"),
        ("0156","100% BANCO"),
        ("0157","DELSUR BANCO UNIVERSAL"),
        ("0163","BANCO DEL TESORO"),
        ("0168","BANCRECER"),
        ("0169","R4 BANCO MICROFINANCIERO C.A."),
        ("0171","BANCO ACTIVO"),
        ("0172","BANCAMIGA BANCO UNIVERSAL, C.A."),
        ("0173","BANCO INTERNACIONAL DE DESARROLLO"),
        ("0174","BANPLUS"),
        ("0175","BANCO DIGITAL DE LOS TRABAJADORES, BANCO UNIVERSAL"),
        ("0177","BANFANB"),
        ("0178","N58 BANCO DIGITAL BANCO MICROFINANCIERO S A"),
        ("0191","BANCO NACIONAL DE CREDITO")
    ]
    STATUS = [
        (0, 'Por confimar'),
        (1, 'Confirmada'),
        (2, 'Rechazada'),
    ]

    lottery = models.ForeignKey("lottery.Lottery", verbose_name=_("Sorteo"), on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.CustomUser", verbose_name=_("Usuario"), on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(_("Cantidad"))
    dollar = models.ForeignKey("lottery.Dollar", verbose_name=_("Tasa del dolar"), on_delete=models.CASCADE, default=1)
    status = models.IntegerField(_("Status"), choices=STATUS, default=0)
    created = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    payment_method = models.IntegerField(_("Método de pago"), choices=PAYMENT_METHOD, default=0)
    
    # Pago móvil
    dni = models.IntegerField(_("Cédula de identidad"), blank=True, null=True)
    type_of_dni = models.IntegerField(_("Tipo de DNI"), choices=TYPE_OF_DNI, blank=True, null=True)
    phone = models.CharField(_("Nro. de teléfono"), max_length=11, validators=[phone_validator], blank=True, null=True)
    bank_code = models.CharField(_("Banco"), max_length=4, choices=BANK_CODE, blank=True, null=True)
    reference = models.IntegerField(_("Nro. de referencia"), blank=True, null=True)
    
    # Zelle/Paypal
    email_or_phone = models.EmailField(_("Email o teléfono"), max_length=254, blank=True, null=True)
    
    amount_bs = models.FloatField(_("Monto Bs."), blank=True, null=True)
    amount_usd = models.FloatField(_("Monto $"), blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.pk}: {self.user.email} lottery-{self.lottery.pk} ({self.quantity})'
    
class Ticket(models.Model):
    number = models.IntegerField(_("Número de ticket"), unique=True)
    order = models.ForeignKey("lottery.Order", verbose_name=_("Orden"), on_delete=models.CASCADE, related_name="tickets")    

    def __str__(self):
        return f'{self.order.lottery.pk} - {self.number}'


@receiver(post_save, sender=Order)
def order_post_save_receiver(sender, instance, created, **kwargs):    
    if created:
        while len(instance.tickets.all()) < instance.quantity:
            available_numbers = set([x for x in range(1, (Lottery.AVAILABLE_TICKETS + 1))]) - set([x.number for x in Ticket.objects.all()])
            Ticket.objects.create(order=instance, number=random.choice(list(available_numbers)))

    else: 
        if instance.status == "2":
            for ticket in instance.tickets.all():
                ticket.delete()
        else:
            while len(instance.tickets.all()) < instance.quantity:
                available_numbers = set([x for x in range(1, (Lottery.AVAILABLE_TICKETS + 1))]) - set([x.number for x in Ticket.objects.all()])
                Ticket.objects.create(order=instance, number=random.choice(list(available_numbers)))

