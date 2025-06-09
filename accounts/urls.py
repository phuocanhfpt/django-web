from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/orders/', views.order_list, name='order_list'),
    path('profile/orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('profile/product-comments/', views.product_comments, name='product_comments'),
    path('profile/post-comments/', views.post_comments, name='post_comments'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    # Password reset (custom view)
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
] 