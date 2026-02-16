from django.urls import path
from . import views

app_name = 'rental'

urlpatterns = [
    path('', views.dashboard_page, name='dashboard'),
    path('apartments/', views.apartment_list_page, name='apartment_list'),
    path('apartments/add/', views.apartment_form_page, name='apartment_add'),
    path('apartments/<int:pk>/', views.apartment_detail_page, name='apartment_detail'),
    path('apartments/<int:pk>/edit/', views.apartment_form_page, name='apartment_edit'),
    path('apartments/<int:pk>/delete/', views.apartment_delete, name='apartment_delete'),
    # Authentication
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_page, name='logout'),
    # API
    path('api/apartments/', views.apartment_api_list, name='apartment_api_list'),
]
