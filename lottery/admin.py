from django.contrib import admin
from .models import Lottery, Order


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

