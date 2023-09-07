from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .email import send_otp_email
from django.core.cache import cache
from . models import *
from store.models import *
from user.views import *
from wishlist.models import *
from user. models import *
from store.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from user.models import User
from django.db.models import Q

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
        
        products=Product.objects.all()
        brands=Brand.objects.all()
        color=Color.objects.all()
        if search_key:
            
           products = products.filter(Q(name__istartswith=search_key)|Q( brand__name__istartswith=search_key)|Q(subcategory__name__istartswith=search_key))

       
        for product in products:
            try:
                product.is_in_wishlist = WishlistItem.objects.filter(product_variant=product.variants.first(), wished_item=request.user.wishlist).exists()  
            except:
                product.is_in_wishlist = False
                # finally:
                #     variants.append(variant)
        if sort:
            if sort == 'low_to_high':
                products = products.annotate(first_variant_selling_price=models.Min('variants__selling_price')).order_by('first_variant_selling_price')
            if sort == 'high_to_low':
                products = products.annotate(first_variant_selling_price=models.Min('variants__selling_price')).order_by('-first_variant_selling_price')



            
        return render(request,'productlist.html',{"products":products,"brands":brands,"color":color})

class productdetail(View):
    def get(self,request,pk):
       
        varient = get_object_or_404(Variant, pk=pk)
        
        
        return render(request,'productdetail.html',{"varient":varient})
    

class userprofile(LoginRequiredMixin,View):
    def get(self,request):
        user_data = UserAddress.objects.filter(user=request.user)
        current_user = User.objects.filter(email=request.user.email).values('name', 'email').first()
        return render(request,'userprofile.html',{'current_user':current_user,'user_data':user_data})


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

        
    


class reset(View):
    def get(self,request):
        return render(request,'reset.html')


class logout_view(View):
    def get(self,request):
        logout(request)  
        return redirect('home')




















