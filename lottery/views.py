from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Lottery, Order, DollarExchangeRate
from .forms import OrderForm, OrderUpdateForm

# Create your views here.
class HomeView(TemplateView):
    template_name = "lottery/home.html"


class LotteryListView(ListView):
    model = Lottery
    template_name = "lottery/_lotteries.html"

    def get_queryset(self):
        return Lottery.objects.filter(closed=False)
    

class LotteryDetailView(DetailView):
    model = Lottery
    template_name = "lottery/lottery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(lottery=self.get_object().pk, user=self.request.user, status=0)
        return context
    

class OrderCreateView(CreateView):
    model = Order
    template_name = "lottery/_order_create.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context["lottery"] = self.request.GET['lottery']
            context["dollar_exchange_rate"] = DollarExchangeRate.objects.get(pk=1).exchange_rate
        context["numbers"] = range(1, 11)
        return context

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Pendiente de revisión')
        return redirect('lottery', self.request.POST['lottery'][0])

    
class OrderUpdateView(UpdateView):
    model = Order
    template_name = "lottery/_order_update.html"
    form_class = OrderUpdateForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.status = 0
        self.object.save()
        messages.success(self.request, 'Modificado con éxito')
        return redirect('order-list')

class OrderListView(ListView):
    model = Order
    template_name = "lottery/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

    


