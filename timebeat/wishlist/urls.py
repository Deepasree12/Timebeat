from django.urls import path
from . import views

urlpatterns=[
    
    path('update_wishlist/<str:pk>/', views.update_wishlist.as_view(), name='wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlistview'),
    
    
]