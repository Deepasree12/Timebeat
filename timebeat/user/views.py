from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .email import send_otp_email
from django.core.cache import cache
from . models import *
from store.models import *
from user.views import *
from cart.views import *
from wishlist.models import *
from user. models import *
from cart. models import *
from store.models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from user.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import razorpay
from timebeat.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET
from django.http import JsonResponse


class index(View):
    def get(self,request):
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        product=Product.objects.all()
        
        return render(request,'index.html',{"category":category,"products":product,"subcategory":subcategory})




class sendotp(View):
    def get(self,request):
        return render(request,'signup.html')

    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered, Please use different email")
            return redirect('signup')
        send_otp_email(email, username, password)
        return redirect('otp')     
       
   
        
class otp_verification(View):
    def get(self,request):
        return render(request, 'otp.html')
    
    def post(self,request):
        received_otp = "".join(request.POST.get(f"otp_{i}", "") for i in range(6))
        if not received_otp:
            messages.error(request, "Please fill OTP.")
        try:
            signup_data = cache.get('signup_data')
            username = signup_data['name']
            email = signup_data['email']
            password = signup_data['password']
            otp = signup_data['otp']
            print(username,email,password,otp,received_otp)
            
        except:
            print('exp')
            messages.error(request, "OTP expired.click resend")
            return redirect('otp')

        if otp == received_otp:  
            myuser = User.objects.create(name=username,email=email)
            myuser.set_password(password)
            myuser.save()
            
            return redirect('signin') 
        else:
            messages.warning(request, "OTP doesn't match.please try again")
            return render(request, 'otp.html')
            

    


class signin(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Invalid email or password')
            return render(request, 'signin.html')
    # Use AuthenticationForm to validate the form data
    # form = AuthenticationForm()
    
    


class productlist(View):
    def get(self,request):
        sort=request.GET.get('sort')
        search_key = request.GET.get('search')
        new_arrivals=request.GET.get('new')
       
        brand_filter = request.GET.getlist('brand_items')
        color_filter = request.GET.getlist('color_items')
        min_price_filter = request.GET.get('min_price')
        max_price_filter = request.GET.get('max_price')
        page_number=request.GET.get('page')
        products=Product.objects.all()
        variant=Variant.objects.all()
        brands=Brand.objects.all()
        colors=Color.objects.all()
        if search_key:
            
           products = products.filter(Q(name__istartswith=search_key)|Q( brand__name__istartswith=search_key)|Q(subcategory__name__istartswith=search_key))

        
      
        variants = []
        for product in products:
            variant = product.variants.order_by('selling_price').first()
            if variant:
                try:
                    variant.is_in_wishlist =  WishlistItem.objects.filter(product_variant=product.variants.first(), wished_item=request.user.wishlist).exists()    
                except:
                    variant.is_in_wishlist = False
                finally:
                    variants.append(variant)
        if brand_filter:
            variants = [variant for variant in variants if variant.product.brand.name in brand_filter]

        if color_filter:
             variants = [variant for variant in variants if variant.color.title in color_filter]

        min_price = None
        max_price = None
        if min_price_filter and max_price_filter:
            min_price = float(min_price_filter)
            max_price = float(max_price_filter)
            products = product.filter(selling_price__gte=min_price,selling_price__lte=max_price)
        price_ranges = [
        {"value": "500-1000", "min": 500, "max": 1000},
        {"value": "1000-2000", "min": 1000, "max": 2000},
        {"value": "2000-3000", "min": 2000, "max": 3000},
        {"value": "3000-4000", "min": 3000, "max": 4000},
        {"value": "4000-5000", "min": 4000, "max": 5000},
        {"value": "5000-", "min": 5000, "max": None},]
        
        if sort:
            if sort == 'low_to_high':
                variants = sorted(variants, key=lambda x: x.selling_price)
            elif sort == 'high_to_low':
                variants = sorted(variants, key=lambda x: x.selling_price, reverse=True)

        if new_arrivals == 'new_arrivals':
            seven_days_ago = datetime.now() - timedelta(days=7)
            products = Product.objects.filter(created_at__gte=seven_days_ago)
            variants = [product.variants.order_by('-created_at').first() for product in products]
        else: 
            products = Product.objects.order_by('-created_at')[:10]  # Get the top 10 most recently added products
            variants = [product.variants.order_by('-created_at').first() for product in products]

        context = {
        'products': products,
        'variants': variants,
        }
        paginator = Paginator(variants, 2)  
        page = paginator.get_page(page_number)
        
        
        return render(request,'productlist.html',{"page":page,"brands":brands,"colors":colors,'brand_filter':brand_filter, 'color_filter':color_filter,'price_ranges': price_ranges,
            'min_price': min_price, 'max_price': max_price,'context':context  })
  

class productdetail(View):
    def get(self,request,pk):
        reviews=0
        rating_data={}
        varient = get_object_or_404(Variant, pk=pk)
        current_user = request.user
        product = varient.product
        reviews = Review.objects.filter(product=product)
        if varient.product.reviews.all():
            reviews = Review.objects.filter(product=varient.product)
            # current_user_review = reviews.filter(user=request.user).first()
        for rating_value in range(5,0,-1):
            rating_count = reviews.filter(rate=rating_value).count()
            try:
                rating_percentage = rating_count/len(reviews)*100 
            except:
                rating_percentage =0
            rating_data[rating_value] = {'count':rating_count,'percentage':rating_percentage}
            reviews.current_user_review=reviews.filter(user=request.user).first() if request.user.is_authenticated else None
        varient.is_in_order=False
        if request.user.is_authenticated:
            for order in request.user.orders.all():
                 for item in order.orderitems.all():
                    if varient.product == item.Product_variant.product:
                        varient.is_in_order = True
                        break
        return render(request,'productdetail.html',{"varient":varient,'current_user':current_user,'reviews':reviews,'rating_data':rating_data,})
    def post(self,request,pk):

        comment = request.POST.get('review')
        rating=request.POST.get('rating')
        variant = get_object_or_404(Variant, pk=pk)
        product = variant.product 
        
        review,created = Review.objects.update_or_create(user=request.user,product=product,
                                                         defaults={'comment':comment, 'rate':rating})
        return redirect(request.META.get('HTTP_REFERER'))
    

class userprofile(LoginRequiredMixin,View):
    def get(self,request):
        user_data = UserAddress.objects.filter(user=request.user)
        current_user = User.objects.filter(email=request.user.email).values('name', 'email').first()
        return render(request,'userprofile.html',{'current_user':current_user,'user_data':user_data})
    

class UserAddAddress(View):
    def post(self, request):
      
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        mobile =request.POST.get('mobile')
        address_type = request.POST.get('address_type')
        place =  request.POST.get('place')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        pincode =request.POST.get('pincode')
        current_user = request.user
        UserAddress.objects.create(name=name,gender=gender,mobile=mobile,address_type=address_type,place=place,
                                    address=address,landmark=landmark,pincode=pincode,user=current_user)

        return redirect('profile')

    
class Checkout(View):
    def get(self, request):
        coupon=Coupon.objects.all()
        user_data = UserAddress.objects.filter(user=request.user)
        user_cart = request.user.cart
        cart_items = CartItem.objects.filter(cart=user_cart)

        current_user = User.objects.filter(email=request.user.email).values('name', 'email').first()
        client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
        payment = client.order.create(dict(amount=request.user.cart.final_price*100,currency="INR",payment_capture=1))
        payment_order_id=payment['id']
        return render(request, 'checkout.html', {
            'current_user': current_user,
            'user_data': user_data,
            'cart':user_cart,
            'cart_items': cart_items,
            'coupons':coupon,
            'payment_API_key':RAZOR_KEY_ID,
            'oder_id':payment_order_id
        })

    def post(self, request):
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        print(payment_method)
        address = UserAddress.objects.get(id=address_id)
        order = Order.objects.create(user=request.user, address=address, payment_mode=payment_method)

        for item in request.user.cart.cartitems.all():
            product_variant = item.product_variant
            total_price = item.total_price
            count = item.count

            OrderItem.objects.create(order=order, Product_variant=product_variant,total_price = total_price,count=count)

        if payment_method == 'cod':
            # messages.success(request, 'Order placed successfully! You have selected Cash on Delivery.')
            order.save()
            return redirect('home')  

        elif payment_method == 'online':
                
            # client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
            # data = { "amount":request.user.Cart.total_selling_price, "currency": "INR","receipt": str(order.id), }
            # payment = client.order.create(data=data)
            # order_id = payment["id"] 
            # order.razorpay_order_id = order_id
            order.status = 'success'
            order.save()
            return redirect('home')
        
        
class ApplyCoupon(View):
    def get(self, request,coupon_code):
        
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        cart = Cart.objects.get(user=request.user)
        if cart.total_selling_price > coupon.minimum_amount:
            cart.coupon_discount_price = coupon.discount_price
        else:
            cart.coupon_discount_price=0
        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))


class OrderHistory(View):
    def get(self, request):
        user_orders = Order.objects.filter(user=request.user)
        
        # Retrieve the order items for the user's orders
        user_order_items = OrderItem.objects.filter(order__in=user_orders)
        
        return render(request, 'orderhistory.html', {'user_orders':user_orders,'user_order_items':user_order_items})

    def post(self,request,pk):

        comment = request.POST.get('review')
        rating=request.POST.get('rating')
        variant = get_object_or_404(Variant, pk=pk)
        product = variant.product 
        
        review,created = Review.objects.update_or_create(user=request.user,product=product,
                                                         defaults={'comment':comment, 'rate':rating})
        return redirect(request.META.get('HTTP_REFERER'))

def change_order_status(request,id):
    order = get_object_or_404(Order, id=id)
    new_status = request.GET.get('status')
    if new_status is not None:
        
        order.status = int(new_status)
        order.save()
    return redirect('orderhistory')
        


class reset(View):
    def get(self,request):
        
        return render(request,'reset.html')


class logout_view(View):
    def get(self,request):
        logout(request)  
        return redirect('home')














 # if payment_method == 'online':
            #     client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET))
            #     data = { "amount": request.user.cart.total_selling_price, "currency": "INR","receipt": str(order.id), }
            #     payment = client.order.create(data=data)
            #     order_id = payment["id"] 
            #     order.razorpay_order_id = order_id
            #     order.status = 'success'
            #     order.save()





