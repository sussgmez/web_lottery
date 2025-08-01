from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("lotteries/", views.LotteryListView.as_view(), name="lotteries"),
    path("lottery/<int:pk>/", views.LotteryDetailView.as_view(), name="lottery"),
    path("lottery/update/<int:pk>/", views.LotteryUpdateView.as_view(), name="lottery-update"),
    path("lottery/create/", staff_member_required(views.LotteryCreateView.as_view()), name="lottery-create"),
    path("lottery/close/<int:pk>/", views.close_lottery, name="lottery-close"),
    path("lottery/open/<int:pk>/", views.open_lottery, name="lottery-open"),
    path("order/list/<int:lottery_pk>/", staff_member_required(views.AdminOrderListView.as_view()), name="admin-order-list"),
    path("order/<int:pk>/", staff_member_required(views.AdminOrderDetailView.as_view()), name="admin-order"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("order/status/<int:pk>/", staff_member_required(views.change_order_status), name="order-status"),
    path("dollar/<int:pk>/", staff_member_required(views.DollarUpdateView.as_view()), name="dollar-update"),
]
