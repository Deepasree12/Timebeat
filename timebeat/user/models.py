from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from . manager import CustomUserManager
from django.db import models
from store.models import *
import uuid
from datetime import timedelta
from datetime import date
from django.utils import timezone



class User(AbstractBaseUser, PermissionsMixin):
  
  id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
  email = models.EmailField(unique=True)
  name=models.CharField(max_length=200 , null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

# @receiver(post_save, sender=User)
# def create_cart_wishlist(sender, instance, created,**kwargs):
#   if created :
#     Cart.objects.create(user=instance)
#     Wishlist.objects.create(user=instance)
  
  
class UserAddress(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=10, choices=[('Mr', 'male'),('Mrs', 'female')])
  mobile = models.CharField(max_length=10)
  address_type = models.CharField(max_length=20, choices=[('house','house'),('office','office')]) 
  place = models.CharField(max_length=100) 
  address = models.CharField(max_length=200)
  landmark = models.CharField(max_length=200)
  pincode = models.CharField(max_length=6)

class Order(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders')
    payment_mode=models.CharField(max_length=250,null=False )
    created_at = models.DateTimeField(auto_now=True)
    expected_delivery = models.DateTimeField(blank=True, null=True,default=timezone.now() + timedelta(days=3))
    total_selling_price = models.IntegerField(default=0)
    total_actual_price = models.IntegerField(default=0) 

    total_discount_price = models.IntegerField(default=0)
    coupon_discount = models.IntegerField(default=0) 
    final_price = models.IntegerField(default=0)

    # @property
    # def total_final_price(self):
    #     return self.aggregate(total_final_price=Sum('final_price'))['total_final_price'] or 0
    def save(self, *args, **kwargs):
        if self.created_at and not self.expected_delivery:
            self.expected_delivery = self.created_at + timedelta(days=3)
        super().save(*args, **kwargs)
    

    
    
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    Product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='orderitems')
    count=models.PositiveSmallIntegerField(default=1)
    total_actual_price = models.IntegerField(default=0)
    status = models.CharField(max_length=100,null=True,default='on the way')
    total_price=models.IntegerField(default=0)



class Review(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
   product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
   comment=models.TextField(max_length=250)
   rate=models.IntegerField(default=0)
   created_at=models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
   id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
   coupon_code=models.CharField(max_length=100,unique=True)
   details=models.CharField(max_length=250)
   count=models.PositiveIntegerField(default=100)
   discount_price=models.IntegerField(default=100)
   minimum_amount=models.IntegerField(default=100)
   start_date=models.DateField(auto_now_add=True)
   end_date=models.DateField(auto_now_add=True)

@property
def status(self):
  if date.today() < self.start_date:
      return "Upcoming"
  elif self.start_date <= date.today() <= self.end_date:
      return "Active"
  else:
      return "Expired"




