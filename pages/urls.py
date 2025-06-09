from django.urls import path
from .views import single_page, dashboard_admin

urlpatterns = [
    path('page/<slug:slug>/', single_page, name='single_page'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
] 