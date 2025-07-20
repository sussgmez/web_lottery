from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('lotteries/', views.LotteryListView.as_view(), name='lotteries'),
    path('lottery/<int:pk>/', views.LotteryDetailView.as_view(), name='lottery'),
    path('order/create/', views.OrderCreateView.as_view(), name='order-create'),
    path('order/update/<int:pk>/', views.OrderUpdateView.as_view(), name='order-update'),
    path('order/detail/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/list/', views.OrderListView.as_view(), name='order-list'),
]
