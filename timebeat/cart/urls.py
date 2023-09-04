from django.urls import path
from . import views

urlpatterns=[
    path('cart/', views.shopping_cart, name='cart'),  
    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'), 
    path('cart_item_increment/<str:pk>/', views.increment_cart, name='increment_cart'), 
    path('cart_item_decrement/<str:pk>/', views.decrement_cart, name='decrement_cart'),
    path('delete_cart_item/<str:pk>/', views.delete_cart, name='delete_cart'),
    
]