from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transfer', views.transfer, name='transfer'),
    # path('deposit',views.deposit,name='deposit'),
    path('deposit/<int:pk>', views.deposit, name='deposit'),
    path('edit/<int:pk>', views.edit_user_details, name='edit'),


]
