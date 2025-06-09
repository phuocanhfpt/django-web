from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('submit/', views.submit_consultation, name='submit'),
    path('newsletter/', views.newsletter_subscription, name='newsletter'),
    path('api/unread-count/', views.unread_consultation_count, name='unread_consultation_count'),
    path('admin/<int:pk>/', views.admin_consultation_detail, name='admin_consultation_detail'),
    path('admin/', views.admin_consultation_list, name='admin_consultation_list'),
    path('', views.contact_view, name='contact'),
] 