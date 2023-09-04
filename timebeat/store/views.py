from django.shortcuts import render,redirect,get_object_or_404
from .models import * 
from user.models import * 
# from .form import Catform

from django.views import View



def adminhome(request):
    return render(request,'adminhome.html')


class user_view(View):
    def get(self,request):
        data=User.objects.all()
        return render(request, 'userlist.html', {'data': data})

    




def adminsignup(request):
    return render(request,'adminsignup.html')




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
        print(cat)
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
       return render(request, 'productsview.html',{'data':data,'p_subcategory':subdata,'brand':brand,'product':product})
       
       
   
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
        variants = specified_product.variant.prefetch_related('variant_images')
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


  


