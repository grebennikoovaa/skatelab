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

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),

    path('checkout/', views.checkout, name='checkout'),
path('shipping/', views.shipping, name='shipping'),
path('payment/', views.payment, name='payment'),
path('order-confirmation/', views.order_confirmation, name='order_confirmation'),

    path('404-preview/', views.custom_404_preview, name='404_preview'),
]