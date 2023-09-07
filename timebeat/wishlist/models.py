from django.db import models
from store.models import *
from user.models import *
import uuid

# Create your models here.

class Wishlist(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    
   def __str__(self):
      return self.id
   

class WishlistItem(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='wishlistitems')
   wished_item=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name='wishlistitems')
   

   def __str__(self):
        return str(self.id)
