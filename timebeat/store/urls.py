from django.urls import path
from . import views



urlpatterns=[
    path('adminhome/',views.adminhome,name='adminhome'),
    path('',views.AdminLogin.as_view(),name='adminlogin'),
    path('adminlogout/',views.AdminLogout.as_view(),name='adminlogout'),
    path('userview/',views.admin_user_managemnt.as_view(),name='userlist'),
    
    path('productview/',views.product_view.as_view(),name='productview'),
    
    path('category/',views.Category_view.as_view(),name='category'),
    path('subcategory/',views.Subcategory_view.as_view(),name='subcategory'),
    path('subcategoryview/',views.subview.as_view(),name='subview'),
    path('brand/',views.Brand_view.as_view(),name='brand'),
    path('admin_order_management/',views.Order_view.as_view(),name='order'),
    
    path('coupon/',views.CouponManagemnet.as_view(),name='coupon'),
    path('color/',views.Color_view.as_view(),name='color'),
    path('product/<str:pk>/',views.Varient_view.as_view(),name='productvarient'),
    path('deliverorder/<uuid:pk>/',views.DeliverOrder.as_view(),name='deliverorder'),
    path('cancelorder/<uuid:pk>/',views.CancelOrder.as_view(),name='cancelorder'),
    path('admin_orderitem_management/<uuid:pk>/',views.AdminOrderItem.as_view(),name='adminorderitem'),
    path('User_access/<uuid:pk>/',views.UserAccess.as_view(),name='useraccess'),
]

