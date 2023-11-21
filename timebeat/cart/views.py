from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from user.views import *
from .models import *
from user. models import *
from store.models import *
from .models import *
from django.views import View
from django.http import HttpResponseBadRequest
import uuid
from django.urls import reverse

def generate_cart_id(request):
    if 'cart_id' not in request.session:
        cart_id = str(uuid.uuid4())  # Generate a unique identifier
        request.session['cart_id'] = cart_id
    return request.session.get('cart_id')


def add_to_cart(request, pk):
    if  not request.user.is_authenticated:
        return redirect('signin')
    if request.user.is_authenticated:
        try:
            variant = Variant.objects.get(pk=pk)
        #     cart = Cart.objects.get_or_create(user=request.user)[0]
        #     cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

        #     if not cart_item_created:
        #         cart_item.count += 1
        #         cart_item.save()

        #     return redirect('productdetail', pk=pk)
        # except Variant.DoesNotExist:
        #     return redirect('not_found')
            cart, cart_created = Cart.objects.get_or_create(user=request.user)

            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

            if not cart_item_created:
                cart_item.count += 1
                cart_item.save()

            return redirect('productdetail', pk=pk)
        except Variant.DoesNotExist:
            return redirect('not_found')
    else:
        try:
            variant = Variant.objects.get(pk=pk)
            cart = request.session.get('cart_id', {})  # Retrieve the cart from session
            cart_item = cart.get(str(variant.id), {'count': 0})

            cart_item['count'] += 1
            cart[str(variant.id)] = cart_item

            request.session['cart_id'] = cart  # Update the cart in session

            return redirect('productdetail', pk=pk)
        except Variant.DoesNotExist:
            return redirect('not_found')
        # if cart := request.session.get('cart'):
        #     print(cart)


 
    
def shopping_cart(request):

    if request.user.is_authenticated:
        user_cart = request.user.cart
        
        if cart_items := CartItem.objects.filter(cart=user_cart).order_by('id'):
    

            return render(request, 'shoping_cart.html', {'cart_items': cart_items,'user_cart':user_cart})
        else:
            return render(request, 'emptycart.html')
    
    else:
        cart = request.session.get('cart_id', {})
        cart_items = []
        subtotal = 0
        total_discount=0
        sub=0
        for variant_id, item_data in cart.items():
            try:
                variant = Variant.objects.get(pk=variant_id)
                total_price = variant.selling_price * item_data['count']
                discount_price = variant.original_price - variant.selling_price

                subtotal += total_price
                total_discount += discount_price
                sub = subtotal - total_discount
                cart_items.append({'variant': variant, 'count': item_data['count'],'total_price': total_price,'discount_price':discount_price})
            except Variant.DoesNotExist:
                pass  

        return render(request, 'shoping_cart.html', {'cart_items': cart_items,'subtotal': subtotal,'total_discount':total_discount,'sub':sub})


def increment_cart(request, pk):
    
    if request.user.is_authenticated:
        
        cart_items = CartItem.objects.get(product_variant_id=pk)
        if cart_items.count  < 10:
            cart_items.count += 1
            cart_items.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        cart = request.session.get('cart_id', {})
        
        try:
            variant = Variant.objects.get(pk=pk)
            cart_items = cart.get(str(variant.id), {'count': 1})
            cart_items['count'] += 1
            
            cart[str(variant.id)] = cart_items
            request.session['cart_id'] = cart
            return redirect(request.META.get('HTTP_REFERER'))
        except Variant.DoesNotExist:
            return HttpResponseBadRequest("Invalid variant")

def decrement_cart(request, pk):

    if request.user.is_authenticated:
       
        cart_item = CartItem.objects.get(product_variant_id=pk)
        # if cart_item.count > 1:
        cart_item.count -= 1
        cart_item.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        cart = request.session.get('cart_id', {})
        
        try:
            variant = Variant.objects.get(pk=pk)
            cart_items = cart.get(str(variant.id), {'count': 0})
            if cart_items['count'] > 1:
                cart_items['count'] -= 1
                cart[str(variant.id)] = cart_items
                request.session['cart_id'] = cart
            else:
                del cart[str(variant.id)]  # Remove the item from the cart if count <= 1
                request.session['cart_id'] = cart
            return redirect(request.META.get('HTTP_REFERER'))
        except Variant.DoesNotExist:
            return HttpResponseBadRequest("Invalid variant")




def delete_cart(request, pk):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product_variant_id=pk)
        cart_item.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        cart = request.session.get('cart_id', {})
        
        try:
            variant = Variant.objects.get(pk=pk)
            if str(variant.id) in cart:
                del cart[str(variant.id)]
                request.session['cart_id'] = cart
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseBadRequest("Item not found in the cart")
        except Variant.DoesNotExist:
            return HttpResponseBadRequest("Invalid variant")






































































