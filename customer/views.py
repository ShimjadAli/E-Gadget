from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,ListView,DetailView
from account.models import Products,Cart,Order
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


#Authentication Decorator
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First")
            return redirect("home")
    return inner

decs=signin_required,never_cache

# Create your views here.


# class CustomerHomeView(View):
#     def get(self,request):
#         res=Products.objects.all()
#         return render(request,"c_home.html",{"data":res})

@method_decorator(decs,name='dispatch')
class CustomerHomeView(ListView):
    template_name="c_home.html"
    queryset=Products.objects.all()
    context_object_name="products"

# class ProductDetailView(View):
#     def get(self,request,**kwargs):
#         pid=kwargs.get('id')
#         prod=Products.objects.get(id=pid)
#         return render(request,"p_details.html",{"data":prod})
    
@method_decorator(decs,name='dispatch')
class ProductDetailView(DetailView):
   template_name="p_details.html"
   pk_url_kwarg="id"
   queryset=Products.objects.all()
   context_object_name="data"

@signin_required
def addcart(request,*args,**kwargs):
    id=kwargs.get("id")
    pro=Products.objects.get(id=id)
    user=request.user
    qty=request.POST.get("qnty")
    Cart.objects.create(product=pro,user=user,quantity=qty)
    messages.success(request,"Added to Cart")
    return redirect('custhome')

@method_decorator(decs,name='dispatch')
class CartListView(ListView):
    template_name="cart.html"
    queryset=Cart.objects.all()
    context_object_name="cart"

    def get_queryset(self):
         return Cart.objects.filter(user=self.request.user,status="cart")

@signin_required   
def removecart(request,**kwargs):
    pid=kwargs.get("id")
    c=Cart.objects.get(id=pid)
    c.delete()
    messages.success(request,"Cart item removed")
    return redirect('cart')

@method_decorator(decs,name='dispatch')
class PaymentView(TemplateView):
    template_name="payment.html"

    def post(self,request,**kwargs):
        cid=kwargs.get("id")
        cart=Cart.objects.get(id=cid)
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        Order.objects.create(cart=cart,address=address,phone=phone)
        cart.status="Order Placed"
        cart.save()
        messages.success(request,"Order Placed Successfully")
        return redirect("cart")

@method_decorator(decs,name='dispatch')
class OrderListView(ListView):
    template_name="orders.html"
    queryset=Order.objects.all()
    context_object_name="order"

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)
    

@signin_required
def cancelorder(request,**kwargs):
    oid=kwargs.get("id")
    order=Order.objects.get(id=oid)
    order.status='Cancelled'
    order.save()
    messages.success(request,"Order Cancelled")
    return redirect("orderlist")

