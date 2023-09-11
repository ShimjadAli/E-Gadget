from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from .models import *
# from django.utils.decorators import method_decorator
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.

class HomeView(FormView):
    template_name="home.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            us=form_data.cleaned_data.get("Username")
            pswd=form_data.cleaned_data.get("Password")
            user=authenticate(request,username=us,password=pswd)
            if user:
                login(request,user)
                messages.success(request,"Login Successful")
                return redirect('custhome')
            else:
                messages.error(request,"Login Failed")
                return redirect("home")
        return render(request,"home.html",{"form":form_data})



class RegView(CreateView):
    template_name="signup.html"
    form_class=RegForm
    model=User
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,"Registration Successful")
        return super().form_valid(form)

# class HomeView(View):
#     def get(self,request):
#         form=LoginForm()
#         return render(request,'home.html',{'form':form})

# class RegView(View):
#     def get(self,request):
#         form=RegForm()
#         return render(request,'signup.html',{'form':form})
#     def post(self,request):
#         form_data=RegForm(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success(request,'Registration Successful..!!')
#             return redirect('home')
#         return render(request,'signup.html',{"form":form_data})


class LgoutView(View):
    def get(self,request):
        logout(request)
        return redirect("home")