from django.db import models
from store.models import *
from user.models import *
import uuid
from django.dispatch import receiver
from django.db.models.signals import *
from django.db.models import Sum


class Cart(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts',default=True)
   total_count = models.PositiveIntegerField(default=0)
   total_selling_price = models.IntegerField(default=0)
   total_actual_price = models.IntegerField(default=0) 
   total_discount_price = models.IntegerField(default=0)
 
   def __str__(self):
      return self.id
    
class CartItem(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='cartitems')
   cart=models.ForeignKey(Cart,on_delete=models.CASCADE,default=None,related_name='cartitems')
   count=models.PositiveSmallIntegerField(default=1)
   total_price = models.IntegerField(default=0)
   total_actual_price = models.IntegerField(default=0)
   discount_price=models.IntegerField(default=0)

   def save(self, *args, **kwargs):
    self.total_price = self.count*self.product_variant.selling_price
    self.total_actual_price = self.count*self.product_variant.original_price
    self.discount_price=self.product_variant.original_price-self.product_variant.selling_price
    super(CartItem, self).save(*args, **kwargs)
   def __str__(self):
        return f'CartItem - {self.id}'

@receiver([post_save, post_delete], sender=CartItem)
def calculate_cart_totals(sender, instance, **kwargs):
   cart = instance.cart
   cart_items = cart.cartitems.all()
   cart.total_count = cart_items.aggregate(Sum('count'))['count__sum'] or 0
   cart.total_selling_price = cart_items.aggregate(Sum('total_price'))['total_price__sum'] or 0
   cart.total_actual_price = cart_items.aggregate(Sum('total_actual_price'))['total_actual_price__sum'] or 0
   cart.total_discount_price = cart.total_actual_price - cart.total_selling_price
   cart.save()