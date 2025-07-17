from django.contrib import admin
from .models import Lottery, Order, Dollar


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['dollar_exchange_rate_calculated', 'total_amount']
    exclude = ['dollar_exchange_rate']

    def dollar_exchange_rate_calculated(self, obj):
        return obj.dollar_exchange_rate.history.as_of(obj.created)
    
    def total_amount(self, obj):
        return obj.dollar_exchange_rate.history.as_of(obj.created).exchange_rate * obj.quantity


@admin.register(Dollar)
class DollarAdmin(admin.ModelAdmin):
    readonly_fields = ['updated']
