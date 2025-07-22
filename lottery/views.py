from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
)
from .models import Lottery, Order, Dollar
from .forms import OrderForm


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
            context["orders"] = Order.objects.filter(
                lottery=self.get_object().pk, user=self.request.user
            )
            context["pending_order"] = Order.objects.filter(
                lottery=self.get_object().pk, user=self.request.user, status=0
            )
        context["dollar"] = Dollar.objects.get(pk=1)
        return context


class OrderCreateView(CreateView):
    model = Order
    template_name = "lottery/_order_create.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            context["lottery"] = Lottery.objects.get(pk=self.request.GET["lottery"])
            context["dollar"] = Dollar.objects.get(pk=1)
        context["select_number"] = range(1, 11)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        print(self.args)

        messages.success(self.request, "Pendiente de revisión")
        return redirect("lottery", self.request.POST["lottery"][0])


class OrderListView(ListView):
    model = Order
    template_name = "lottery/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = "lottery/_order_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dollar"] = Dollar.objects.get(pk=1).history.as_of(
            self.get_object().created
        )
        return context


class OrderAdminListView(ListView):
    model = Order
    template_name = "lottery/_order_admin_list.html"

    def get_queryset(self):

        return (
            Order.objects.filter(lottery=self.kwargs["pk"])
            .filter(reference__contains=self.request.GET["filter"])
            .order_by("status")
        )


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
        "lottery/_order_admin.html",
        context={"order": Order.objects.get(pk=pk)},
    )


def get_emails(request, pk):
    lottery = Lottery.objects.get(pk=pk)
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = (
        f'attachment; filename="{lottery.description}.txt"'
    )

    text = ""
    orders = Order.objects.filter(lottery=lottery.pk, status=1)

    for order in orders:
        for x in range(0, order.quantity):
            text += order.user.email + "\n"

    response.write(text)

    return response
