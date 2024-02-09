from django.urls import path
from . import views
urlpatterns = [
    path('convert/', views.convert),
    path('charges/', views.getWithdrawCharges),
    path('verify_me/', views.notifyAdminForVerification),
]