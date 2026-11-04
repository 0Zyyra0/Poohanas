"""URL configuration for the Store app."""
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.checkout_process, name='checkout_process'),
    path('checkout/confirmation/<str:order_number>/', views.checkout_confirmation, name='checkout_confirmation'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),

    # Wishlist
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/add/<int:product_id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', views.wishlist_remove, name='wishlist_remove'),

    # Reviews
    path('products/<slug:slug>/review/', views.add_review, name='add_review'),

    # Account
    path('account/', views.account_dashboard, name='account_dashboard'),

    # Contact
    path('contact/', views.contact, name='contact'),
]