from django.contrib import admin
from django.urls import path
from.views import*
from.import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.log,name='login'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.Contact,name='contact'),
    path('home/',views.Home,name='home'),
    path('shop/',views.shop,name='shop'),
    path('shopdetail/', views.shopdetail, name='shop-detail'),
    path('testimonial/', views.Testimonial, name='testimonial'),
    path('remove-cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('plus-cart/<int:product_id>/', views.plus_cart, name='plus_cart'),
    path('minus-cart/<int:product_id>/', views.minus_cart, name='minus_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirm/', views.orderconfirm, name='order_confirm'),
    path('search_item/', views.search_item, name='search_item'),
    
]
    
    
    
    
    
    
    
    
    
    
    

