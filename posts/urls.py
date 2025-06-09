from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('danh-muc/<slug:slug>/', views.post_list_by_category, name='post_list_by_category'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<str:tag_slug>/', views.post_list_by_tag, name='tag_list'),
] 