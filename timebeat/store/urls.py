from django.urls import path
from . import views



urlpatterns=[
    path('',views.adminhome,name='adminhome'),
    path('adminsignup/',views.adminsignup,name='adminsignup'),
    path('userview/',views.user_view.as_view(),name='userlist'),
    
    path('productview/',views.product_view.as_view(),name='productview'),
    
    path('category/',views.Category_view.as_view(),name='category'),
    path('subcategory/',views.Subcategory_view.as_view(),name='subcategory'),
    path('subcategoryview/',views.subview.as_view(),name='subview'),
    path('brand/',views.Brand_view.as_view(),name='brand'),
    path('color/',views.Color_view.as_view(),name='color'),
    path('product/<str:pk>/',views.Varient_view.as_view(),name='productvarient'),

]