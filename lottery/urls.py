from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("lotteries/", views.LotteryListView.as_view(), name="lotteries"),
    path("lottery/<int:pk>/", views.LotteryDetailView.as_view(), name="lottery"),
    path("lottery/close/<int:pk>/", views.close_lottery, name="lottery-close"),
    path("lottery/open/<int:pk>/", views.open_lottery, name="lottery-open"),
    path("order/list/<int:lottery_pk>/", views.AdminOrderListView.as_view(), name="admin-order-list"),
    path("order/<int:pk>/", views.AdminOrderDetailView.as_view(), name="admin-order"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("order/status/<int:pk>/", views.change_order_status, name="order-status"),
]
