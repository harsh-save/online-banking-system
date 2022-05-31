from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin_panel', views.admin_landing, name="admin_main"),
    path('register', views.register, name="register_user"),
    path('transactions', views.transactions, name="transactions"),
    path('username_validate', views.generate_username, name='generate_username'),
    path('admin_login', views.admin_login, name="admin_login"),
    path('feedback_view', views.feedback_view, name='feedback_view'),
    path('accounts/<int:pk>', views.account_details, name='accounts'),
    path('report', views.admin_report, name='report'),

]
