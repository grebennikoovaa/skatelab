from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('complete-skateboards/', views.complete_skateboards, name='complete_skateboards'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]