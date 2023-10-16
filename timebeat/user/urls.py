from django.urls import path
from . import views
from wishlist import *

urlpatterns=[
    path('',views.index.as_view(),name='home'),
    path('signin/',views.signin.as_view(),name='signin'),
    path('signup/',views.sendotp.as_view(),name='signup'),
    path('otp/',views.otp_verification.as_view(),name='otp'),
    path('forgot_password/',views.ForgotPassword.as_view(),name='forgot'),
    path('reset_here/<str:encrypt_id>/',views.UserResetPassword.as_view(),name='resetpassword'),
    path('productlist/',views.productlist.as_view(),name='productlist'),
    path('userprofile/',views.userprofile.as_view(),name='profile'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('order_history/',views.OrderHistory.as_view(),name='orderhistory'),
    path('logout/',views.logout_view.as_view(),name='logout'),
    path('applycoupon/<str:coupon_code>',views.ApplyCoupon.as_view(),name='applycoupon'),
    path('UserAddAddress/',views.UserAddAddress.as_view(),name='addAddress'),
    path('productview/<uuid:pk>/', views.productdetail.as_view(), name='productdetail'),
    path('invoice/<uuid:pk>/',views.Invoice.as_view(),name='invoice'),
    path('review/<uuid:pk>/',views.ReviewUpdate.as_view(),name='reviewupdated'),
    path('productcategory/<str:category>/',views.CategoryProductList.as_view(),name='catgoryproducts'),
    
]