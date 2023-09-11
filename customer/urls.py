from django.urls import path
from .views import*

urlpatterns = [
    path('cust',CustomerHomeView.as_view(),name="custhome"),
    path('pdetails/<int:id>',ProductDetailView.as_view(),name="pdetails"),
    path('cart',CartListView.as_view(),name="cart"),
    path('acart/<int:id>',addcart,name="acart"),
    path('rcart/<int:id>',removecart,name="rcart"),
    path('payment/<int:id>',PaymentView.as_view(),name="payment"),
    path('orderlist',OrderListView.as_view(),name="orderlist"),
    path('cancel/<int:id>',cancelorder,name="cancel"),
]
