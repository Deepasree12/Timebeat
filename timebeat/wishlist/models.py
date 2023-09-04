from django.db import models
from store.models import *
from user.models import *
import uuid

# Create your models here.

class Wishlist(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlists',default=True)
    
   def __str__(self):
      return self.id
   

class WishlistItem(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='wishlistitems')
   wished_item=models.ForeignKey(Wishlist,on_delete=models.CASCADE,default=None,related_name='wishlistitems')
   added_date = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.wished_item.id
