from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from . manager import CustomUserManager
from django.db import models
from store.models import *
import uuid


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
  

# class Cart(models.Model):
#     id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
#     user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    
# class CartItem(models.Model):
#    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
#    product_variant=models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='cartitem')
#    count=models.IntegerField(default=1)