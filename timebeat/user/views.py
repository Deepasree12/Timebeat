from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .email import send_otp_email
from django.core.cache import cache
from . models import *
from store.models import *
from store.models import Product,Category,Subcategory
from django.shortcuts import get_object_or_404
from django.views import View






class index(View):
    def get(self,request):
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        product=Product.objects.all()
        
        return render(request,'index.html',{"category":category,"products":product,"subcategory":subcategory})
# @login_required(login_url='signin')//add in wishlist



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
        product=Product.objects.all()
        return render(request,'productlist.html',{"products":product})

class productdetail(View):
    def get(self,request,pk):
       
        varient = get_object_or_404(Variant, pk=pk)
        
        
        return render(request,'productdetail.html',{"varient":varient})


class reset(View):
    def get(self,request):
        return render(request,'reset.html')


class logout_view(View):
    def get(self,request):
        logout(request)  
        return redirect('home')




















# Create your views here.

# def signup_user(request):

#   if request.method == 'POST':
#     name = request.POST.get('name')
#     email = request.POST.get('email')
#     password = request.POST.get('pass')
#     userobj = User.objects.filter(email=email)
#     if userobj.exists():
#       messages.warning(request , 'You are already registerd, Please sign in')
#       return redirect(signup_user)
#     send_otp_email(email, name, password)
#     return redirect(verify_otp)
#   return render(request , 'user_signup.html')


# def verify_otp(request):
#   if request.method == 'POST':
#     reciveotp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + request.POST.get('otp4') + request.POST.get('otp5') + request.POST.get('otp6')
#     try:
#       name = cache.get('signup_data')['name']
#       email = cache.get('signup_data')['email']
#       password = cache.get('signup_data')['password']
#       otp = cache.get('signup_data')['otp']
#     except:
#       messages.warning(request,'otp exipred')
#       return redirect(verify_otp)
#     print(otp,reciveotp)
#     if reciveotp != otp:
#       messages.warning(request , 'OTP mismatch')
#       return redirect(verify_otp)
#     User.objects.create_user(name = name , email = email , password=password)
#     cache.clear()
#     return redirect(signin)
#   return render(request , 'user_verify_otp.html')

# def signin(request):

#   if request.method == 'POST':
#     email = request.POST.get('email')
#     password = request.POST.get('pass')
#     print(email,password)
#     user = authenticate(request, email=email,password=password)
#     print(user)
#     if user is not None:
#       login(request, user)
#       request.session['usr_id'] = user.id
#     messages.warning(request , 'Email password mismatch')
#   return render( request , 'user_signin.html')


# def signout(request):
#   logout(request)
#   return redirect(signin)