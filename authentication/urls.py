from . import  views
from django.urls import path

urlpatterns = [
    path('', views.Auth.as_view()),
    path('resend_link/', views.resend_link),
    path('psreset_link/', views.psreset_link),
    path('reset/', views.reset),
    path('verify/', views.verify_account),
]