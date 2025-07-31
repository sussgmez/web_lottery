from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Lottery, Order, Dollar, Ticket
from .forms import Order1Form, Order2Form, LotteryForm


class HomeView(TemplateView):
    template_name = "lottery/home.html"


class LotteryListView(ListView):
    model = Lottery
    template_name = "lottery/_lotteries.html"


class LotteryDetailView(DetailView):
    model = Lottery
    template_name = "lottery/lottery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_tickets"] = Ticket.objects.filter(
                order__user=self.request.user,
                order__lottery=self.get_object(),
                order__status=1,
            )
            context["available_tickets"] = Lottery.AVAILABLE_TICKETS - len(
                Ticket.objects.filter(order__lottery=context["lottery"].pk)
            )

        context["dollar"] = Dollar.objects.get(pk=1)

        return context


class LotteryUpdateView(UpdateView):
    model = Lottery
    template_name = "lottery/_lottery_update.html"
    form_class = LotteryForm

    def form_valid(self, form):
        self.object.save()
        return redirect("lottery", self.object.pk)


class OrderCreateView(CreateView):
    model = Order
    template_name = "lottery/_order_create.html"

    def get_form_class(self):
        if self.request.GET["payment_method"] == "0":
            return Order1Form
        return Order2Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lottery"] = Lottery.objects.get(pk=self.request.GET["lottery"])
        context["payment_method"] = self.request.GET["payment_method"]
        available_tickets = Lottery.AVAILABLE_TICKETS - len(
            Ticket.objects.filter(order__lottery=context["lottery"].pk)
        )
        context["available_tickets"] = (
            range(1, (available_tickets + 1))
            if available_tickets < 10
            else range(1, 11)
        )
        context["pending_order"] = Order.objects.filter(
            lottery=self.request.GET["lottery"], user=self.request.user, status=0
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(
            f".?payment_method={self.object.payment_method}&lottery={self.object.lottery.pk}"
        )


class AdminOrderListView(ListView):
    model = Order
    template_name = "lottery/_admin_order_list.html"

    def get_queryset(self):
        filter = self.request.GET['filter']
        print(filter)
        return Order.objects.filter(lottery=self.kwargs["lottery_pk"]).filter(user__email__contains=filter) | Order.objects.filter(lottery=self.kwargs["lottery_pk"]).filter(tickets__number__contains=filter)

class AdminOrderDetailView(DetailView):
    model = Order
    template_name = "lotteryt/_admin_order.html"

def close_lottery(request, pk):
    lottery = Lottery.objects.get(pk=pk)
    lottery.closed = True
    lottery.save()

    return redirect("lottery", pk=pk)


def open_lottery(request, pk):
    lottery = Lottery.objects.get(pk=pk)
    lottery.closed = False
    lottery.save()

    return redirect("lottery", pk=pk)


def change_order_status(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = request.GET["status"]
    order.save()

    return render(
        request,
        "lottery/_admin_order.html",
        context={"order": Order.objects.get(pk=pk)},
    )
