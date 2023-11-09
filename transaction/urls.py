from . import  views
from django.urls import path

urlpatterns = [
    path('getTransact/', views.getTransact),
    path('deposit/', views.deposit),
    path('invest/', views.invest),
    path('withdraw/', views.withdraw),
    # path('psreset_link/', views.psreset_link),
    # path('reset/', views.reset),
    # path('verify/', views.verify_account),
]