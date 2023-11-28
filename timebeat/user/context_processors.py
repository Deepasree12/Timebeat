from cart.models import *
from wishlist.models import *

def calculate_count(request):
  if request.user.is_authenticated:
    cartitems=CartItem.objects.filter(cart=request.user.cart)
    wishlist=WishlistItem.objects.filter(wished_item=request.user.wishlist)
    return {"cartitems":cartitems,"wishlist":wishlist}