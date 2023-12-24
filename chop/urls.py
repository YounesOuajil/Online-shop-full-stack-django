from django.urls import path
from . import views

urlpatterns=[
    path('', views.store, name='store'),
    path('USER_register/',views.USER_register,name='register'),
    path('USER_login/',views.USER_login,name='login'),
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('homeUser/', views.homeUser, name='homeUser'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.logout_view, name='logout'),
    path('update_cart/',views.update_cart, name='update_cart'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/',views.products,name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/update/', views.update_product, name='update_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('up_products/', views.up_products, name='up_products'),
    path('send_order/',views.send_order,name='send_order'),
    path('order_list/',views.order_list,name='order_list'),
    path('store_search/', views.store_search, name='store_search'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),



    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),





]

	   