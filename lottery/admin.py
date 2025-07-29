from django.contrib import admin
from .models import Lottery, Order, Dollar, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass



@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ['lottery_price', 'exchange_rate', 'total_amount']
    # exclude = ['dollar']

    # def lottery_price(self, obj):
    #     return obj.lottery.price
    
    # def exchange_rate(self, obj):
    #     return f'{obj.dollar.history.as_of(obj.created)} $ - {obj.created.strftime("%d/%m/%Y")}'
    
    # def total_amount(self, obj):
    #     return f'{obj.dollar.history.as_of(obj.created).exchange_rate * obj.quantity *  obj.lottery.price} Bs'


@admin.register(Dollar)
class DollarAdmin(admin.ModelAdmin):
    readonly_fields = ['updated']
