from django.shortcuts import get_object_or_404, redirect


from user.views import *
from .models import *
from user. models import *
from store.models import *
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Wishlist, WishlistItem

class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        
        user_wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        
        
        wishlist_items = WishlistItem.objects.filter(wished_item=user_wishlist)

        if wishlist_items:
            return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
        else:
            return render(request, 'emptywishlist.html')



class update_wishlist(LoginRequiredMixin,View):
    def get(self, request, pk):
        variant = Variant.objects.get(id=pk)
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_item, wishlist_item_created = WishlistItem.objects.get_or_create(wished_item=wishlist, product_variant=variant)
               
        if not wishlist_item_created:          
            wishlist_item.delete()               
        return redirect(request.META.get('HTTP_REFERER'))
    