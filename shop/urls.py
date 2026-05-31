from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),

    path('categories/', views.categories, name='categories'),
    path('complete-skateboards/', views.complete_skateboards, name='complete_skateboards'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]