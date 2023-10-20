from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from .models import * 
from user.models import * 
from django.http import JsonResponse
from django.db.models import Sum,Count
from datetime import date
from django.db.models.functions import TruncMonth
from django.views import View
from cart.models import * 



def adminhome(request):
    cancelled = OrderItem.objects.filter(status='Cancelled')
    delivered = OrderItem.objects.filter(status='Delivered')
    pending = OrderItem.objects.filter(status='on the way')
    order=Order.objects.all()
    customers=User.objects.filter(is_superuser=False)
    products=Product.objects.all()
    total_revenue = Order.objects.aggregate(total_revenue=Sum('final_price'))['total_revenue']
    monthly_revenue = Order.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_revenue=Sum('final_price'),
        order_count=Count('id')
    ).order_by('month')
   
    return render(request, 'adminhome.html', {
        'pending': pending,
        'cancelled': cancelled,
        'delivered': delivered,
        'order':order,
        'customers':customers,
        'products':products,
        'total_revenue':total_revenue,
        'monthly_revenue':monthly_revenue

    })
class admin_user_managemnt(View):
    def get(self,request):
        users=User.objects.filter(is_superuser=False)
        return render(request, 'adminusers.html', {'users': users}
                      )
class UserAccess(View):
    def get(self,request,pk):
        user=User.objects.get(id=pk)
        if user.is_active == True:
            user.is_active=False
        else:                                                                       
            user.is_active=True
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))

    
def adminsignup(request):
    return render(request,'adminsignup.html')

class AdminLogout(View):
    def get(self,request):
        logout(request)  
        return redirect('adminhome')


class Category_view(View):

    def get(self, request):
        data=Category.objects.all()
        return render(request, 'category.html',{'data':data})

    def post(self, request):
        name = request.POST.get('category')
        Category.objects.create(name=name)
        return redirect('category')
            
    



class Subcategory_view(View):
    def get(self,request): 
        
        p_category = Category.objects.all()
        return render(request, 'subcategory.html',{'p_category':p_category})


    def post(self, request):
      
        name = request.POST.get('sub')
        cat = request.POST.get('category')
        image = request.FILES.get('image')
       
        try:
            category = Category.objects.get(id=cat)
        except:
            print('caregory does not exist')
        Subcategory.objects.create(name=name, image=image, category=category)

        return redirect('subview')
  

class subview(View):
    def get(self,request):
        data=Subcategory.objects.all()
        return render(request, 'subcatlist.html', {'data': data})


class Brand_view(View):

    def get(self, request):
        data=Brand.objects.all()
        return render(request, 'brand.html',{'data':data})

    def post(self, request):
        name = request.POST.get('brand')
        Brand.objects.create(name=name)
        return redirect('brand')
    





class product_view(View):
    def get(self,request): 
        
       data=Category.objects.all()
       subdata=Subcategory.objects.all()
       brand=Brand.objects.all()
       product=Product.objects.all()
       
       return render(request, 'productsview.html',{'data':data,'p_subcategory':subdata,'brand':brand,'product':product,})
       
       
   
    def post(self, request):
      
        name = request.POST.get('product')
        cat = request.POST.get('category')
        subcat = request.POST.get('subcategory')
        brand=request.POST.get('brand')
        
        
        details = request.POST.get('details')
        
        
        category = Category.objects.get(id=cat)
        subcategory =Subcategory.objects.get(id=subcat)
        brand=Brand.objects.get(id=brand)
        
        Product.objects.create(name=name, category=category,subcategory=subcategory,description=details,brand=brand)

        return redirect('productview')



class Color_view(View):

    def get(self, request):
        data=Color.objects.all()
        return render(request, 'color.html',{'data':data})

    def post(self, request):
        name = request.POST.get('colorname')
        code = request.POST.get('colorcode')
        Color.objects.create(title=name,code=code)
        return redirect('color')
    
class Varient_view(View):
    def get(self,request,pk):
        
        
        specified_product = get_object_or_404(Product, id=pk)
        variants = specified_product.variants.prefetch_related('variant_images')
        colors=Color.objects.all()
        
        return render(request, 'productvarient.html',{'colors':colors,'product':specified_product,'variants':variants})
    
    def post(self, request,pk):
        
        
        clr = request.POST.get('color')
        
        image = request.FILES.get('image')
        stock=request.POST.get('stock')
        color = Color.objects.get(id=clr)
        product = Product.objects.get(id=pk)
        subimages = request.FILES.getlist('subimage')
        original = request.POST.get('original')
        selling = request.POST.get('selling')
        varient=Variant.objects.create(mainimage=image,stock=stock,color=color,product=product,original_price=original,selling_price=selling)
        
        for image in subimages:
            Images.objects.create(image=image,varient=varient)

        return redirect('productvarient',pk=pk)



class CouponManagemnet(View):
    def get(self,request):

        current_date = datetime.today().strftime("%Y-%m-%d")
        return render(request, 'admincoupon.html',{'current_date':current_date})
    
    def post(self,request):
        coupon_code = request.POST.get('coupon')
        details = request.POST.get('coupondetails')
        count = request.POST.get('couponcount')
        discount_price=request.POST.get('discount')
        minimum=request.POST.get('minimum')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        Coupon.objects.create(coupon_code=coupon_code, details=details, count=count,discount_price=discount_price,minimum_amount=minimum,start_date=startdate,end_date=enddate)
        return redirect('coupon')


class Order_view(View):

    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'adminorder.html', {'orders': orders})

    def post(self, request):
        order_id = int(request.POST.get('order_id'))
        status = request.POST.get('status')
        return redirect('order') 

class AdminOrderItem(View):
    def get(self,request,pk):
        order = get_object_or_404(Order, id=pk)
        orderitems=order.order_items.all()
        return render(request, 'admin_order_item.html', {'orderitems': orderitems})

class DeliverOrder(View):
    def get(self,request,pk):
        orderitem=OrderItem.objects.get(id=pk)
        orderitem.status = 'Delivered'
        orderitem.save()
        return redirect(request.META.get('HTTP_REFERER'))
class CancelOrder(View):
    def get(self,request,pk):
        orderitem=OrderItem.objects.get(id=pk)
        orderitem.status='Cancelled'
        orderitem.save()
        return redirect(request.META.get('HTTP_REFERER'))
        
        