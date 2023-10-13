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
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.db.models import Min,Max


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
        
        if user is not None :
            if user.is_active == True :
                login(request, user)
            else:
                messages.warning(request, 'user is bannned')
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
        min_limit=request.GET.get('min')
        max_limit=request.GET.get('max')
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

        
        
        if sort:
            if sort == 'low_to_high':
                variants = sorted(variants, key=lambda x: x.selling_price)
            elif sort == 'high_to_low':
                variants = sorted(variants, key=lambda x: x.selling_price, reverse=True)
                
        if new_arrivals == 'new_arrivals':
            variants.sort(key=lambda x:x.product.created_at)
        else: 
            products = Product.objects.order_by('-created_at')[:10]  # Get the top 10 most recently added products
            variants = [product.variants.order_by('-created_at').first() for product in products]
        # if min_limit and max_limit:
        #     if max_limit == '10000':
        #         variants = [variant for variant in variants if min_limit and int(min_limit) < variant.selling_price]
        #     else:
        #         variants = [variant for variant in variants if min_limit and max_limit and int(min_limit) < variant.selling_price < int(max_limit)]
        context = {
        'products': products,
        'variants': variants,
        }
        paginator = Paginator(variants, 2)  
        page = paginator.get_page(page_number)
        
        
        return render(request,'productlist.html',{"page":page,"brands":brands,"colors":colors,'brand_filter':brand_filter, 'color_filter':color_filter,
        'context':context  })
  

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
                 for item in order.order_items.all():
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
        cart=request.user.cart
        cart.coupon_discount_price = request.session.get('coupon_discount',0)
        if cart.total_selling_price > cart.coupon_discount_price:
            cart.final_price = cart.total_selling_price-cart.coupon_discount_price
        else:
            cart.coupon_discount_price=0
            cart.final_price=cart.total_selling_price
        cart.save()
        try:
            del request.session['coupon_discount']
        except KeyError:
            pass
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
        cart=request.user.cart
       
        address = UserAddress.objects.get(id=address_id)
        order = Order.objects.create(user=request.user, address=address, payment_mode=payment_method,total_discount_price=cart.total_discount_price,
                                     coupon_discount=cart.coupon_discount_price,total_selling_price=cart.total_selling_price,
                                     final_price=cart.final_price,total_actual_price=cart.total_actual_price)
        
        
        
        for item in request.user.cart.cartitems.all():
            product_variant = item.product_variant
            
            total_price = item.total_price
            count = item.count
            total_actual_price=item.total_actual_price
            OrderItem.objects.create(order=order, Product_variant=product_variant,total_price = total_price,count=count,total_actual_price=total_actual_price)
            

        request.user.cart.cartitems.all().delete()
        messages.success(request,'order placed')
        return redirect('home')
        
        
class ApplyCoupon(View):
    def get(self, request,coupon_code):
        
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()
        cart = request.user.cart
        
        if cart.total_selling_price > coupon.minimum_amount:
            request.session['coupon_discount'] = coupon.discount_price
        messages.success(request, "Coupon is applied")
        return redirect(request.META.get('HTTP_REFERER'))

class OrderHistory(View):
    def get(self, request):
        
        user_orders = Order.objects.filter(user=request.user)
        all_order_items = []
        for order in user_orders:
            for item in order.order_items.all():
                item.review = Review.objects.filter(user=request.user,product=item.Product_variant.product).first()
                all_order_items.append(item)
        return render(request, 'orderhistory.html', {'user_order_items':all_order_items})
    
class ReviewUpdate(View):
    def post(self, request, pk):
    
        comment = request.POST.get('review')
        rating = request.POST.get('rating')
        
        product = get_object_or_404(Product, pk=pk)
    

        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'comment': comment, 'rate': rating}
        )
        

        return redirect(request.META.get('HTTP_REFERER'))

class Invoice(View):
    def get(self,request,pk):
       
        order = get_object_or_404(Order, id=pk)
        orderitems=order.order_items.all()
        template_path = 'invoice.html'
        context = {
          'order':order,
          'orderitems':orderitems,

        }
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

        # Create PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


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





