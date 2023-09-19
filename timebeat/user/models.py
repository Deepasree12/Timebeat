from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from . manager import CustomUserManager
from django.db import models
from store.models import *
import uuid
from datetime import datetime, timedelta



class User(AbstractBaseUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
  email = models.EmailField(unique=True)
  name=models.CharField(max_length=200 , null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def __str__(self):
      return self.name
  
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
   orderstatuses=(
       ('pending','pending'),
       ('Out For Shipping','Out For Shipping'),
       ('Deliverd','Deliverd'),
       ('cancelled','cancelled'),
       ('returned','returned')
       )
   status=models.CharField(max_length=150,choices=orderstatuses,default='pending')
   message=models.TextField(null=True)
   created_at = models.DateTimeField(auto_now=True)
   expected_delivery = models.DateTimeField(blank=True, null=True)

   def save(self, *args, **kwargs):
        if self.created_at and not self.expected_delivery:
            self.expected_delivery = self.created_at + timedelta(days=3)
        super().save(*args, **kwargs)
   
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderitems')
    Product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='orderitems')
    count=models.PositiveSmallIntegerField(default=1)
    total_price = models.IntegerField(default=0)
   







#  payment_id=models.CharField(max_length=250,null=True)
 
  #  status=models.CharField(max_length=150,choices=orderstatuses,default='pending')
  #  message=models.TextField(null=True)
  #  tracking_no=models.CharField( max_length=250,null=True)
  #  created_at=models.DateTimeField(auto_now=True)

  #  def __str__(self):
  #     return '{} - {}'.format(self.id,self.tracking_no)




    # def __str__(self):
    #   return '{} - {}'.format(self.order.id,self.tracking_no)

# class PaymentMethod(models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

