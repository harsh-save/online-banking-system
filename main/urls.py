from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('accountdetails', views.account_page, name='account_page'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('transaction_hist', views.transaction_history, name='history'),
    path('otp', views.otp, name='otp'),
    path('feedback', views.feedback, name='feedback'),
    path('edit', views.edit_details, name='edit'),
    path('statement', views.statement, name='statement'),
    path('about_us', views.about_us, name='about_us'),
    #####
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='landing/pass_change/password_reset_form.html'),
         name='password_reset'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='landing/pass_change/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='landing/pass_change/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='landing/pass_change/password_reset_complete.html'), name='password_reset_complete'),
    #path('reset-password-done', PasswordResetDoneView, name='password_reset_done'),
    #######
    #path('password_reset', auth_views.PasswordChangeForm, name='password_reset'),
    #path('acc/', include('django.contrib.auth.urls')),



]
