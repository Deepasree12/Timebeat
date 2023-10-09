from django.urls import path
from . import views
from wishlist import *

urlpatterns=[
    path('',views.index.as_view(),name='home'),
    path('signin/',views.signin.as_view(),name='signin'),
    path('signup/',views.sendotp.as_view(),name='signup'),
    path('otp/',views.otp_verification.as_view(),name='otp'),
    path('reset/',views.reset.as_view(),name='reset'),
    path('productlist/',views.productlist.as_view(),name='productlist'),
    path('userprofile/',views.userprofile.as_view(),name='profile'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('order_history/',views.OrderHistory.as_view(),name='orderhistory'),
    # path('change-order-status/', views.change_order_status, name="change_order_status"),
    path('orderdetail/',views.OrderDetails.as_view(),name='orderdetail'),
    path('logout/',views.logout_view.as_view(),name='logout'),
    path('applycoupon/<str:coupon_code>',views.ApplyCoupon.as_view(),name='applycoupon'),
    path('UserAddAddress/',views.UserAddAddress.as_view(),name='addAddress'),
    path('productview/<uuid:pk>/', views.productdetail.as_view(), name='productdetail'),
    path('invoice/<uuid:pk>/',views.Invoice.as_view(),name='invoice'),
    #  path('download_invoice/',views.generate_pdf.as_view(),name='pdf'),
]