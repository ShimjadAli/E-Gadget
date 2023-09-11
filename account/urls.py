from django.urls import path
from.views import *


urlpatterns = [
    # path('lg',LoginView.as_view(),name='login'),
    path('reg',RegView.as_view(),name='reg'),
    path('logout',LgoutView.as_view(),name='logout'),
]
