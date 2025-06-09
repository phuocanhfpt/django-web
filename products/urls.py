from django.urls import path
from . import views
from .views import ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.contact, name='contact'),
    # path('register/', views.register, name='register'),  # Đã chuyển sang accounts app
    path('search/', views.search_results, name='search_results'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-password/done/', views.password_change_done, name='password_change_done'),
    path('sitemap-modal/', views.sitemap_modal, name='sitemap_modal'),
    path('sitemap/', views.sitemap_modal, name='sitemap'),
] 