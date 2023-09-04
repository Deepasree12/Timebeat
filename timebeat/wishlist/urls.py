from django.urls import path
from . import views

urlpatterns=[
    path('wishlist/', views.add_to_wishlist, name='wishlist'),  
    
    
    
]