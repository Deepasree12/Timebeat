from django.db import models
import uuid
from django.db.models import Avg
# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   
    name = models.CharField(max_length=200,null=False,blank=False)
    

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    
    name = models.CharField(max_length=200,null=False,blank=False)
    image=models.ImageField(upload_to="storeimages/",null=True,blank=True)
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    
    name = models.CharField(max_length=200,null=False,blank=False)
    def __str__(self):
        return self.name

    
class Product(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  
    
    name = models.CharField(max_length=300,null=False,blank=False)
    
    description = models.CharField(max_length=500,null=True,blank=True)
    created_at=models.DateTimeField(auto_now=True)
    
   
    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rate'))['rate__avg']


    




class Color(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.CharField(max_length=300)
    code = models.CharField(max_length=300)  

    def __str__(self):
        return self.title

class Variant(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    
    stock=models.IntegerField(null=True)
    mainimage = models.ImageField(upload_to="images",null=True,blank=True)
    color=models.ForeignKey(Color, on_delete=models.CASCADE,null=True,related_name="variants")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    original_price=models.FloatField(null=True)
    selling_price=models.FloatField(null=True)
    created_at=models.DateTimeField(auto_now=True)
   
    # def __str__(self):
    #     return self.name

class Images(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    varient=models.ForeignKey(Variant, on_delete=models.CASCADE,null=True,related_name="variant_images")
    def __str__(self):
        return self.name


