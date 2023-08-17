# from django.contrib import admin
# from .models import Category,Subcategory,Brand,Product
# # Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id',  'name']
#     search_fields = ['name', ]

# class SubcategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'category']
#     list_filter = ['category']
#     search_fields = ['name', 'category__name']

# class BrandAdmin(admin.ModelAdmin):
#     list_display = ['id',  'name','category','subcategory']
#     search_fields = ['name', 'category__name','subcategory__name']

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'category', 'subcategory', 'brand', 'original_price','selling_price','quantity' ]  
#     search_fields = ['name', 'category__name', 'brand__name', 'subcategory__name']  
#     # prepopulated_fields = { ('name',)}


# admin.site.register(Category,CategoryAdmin)
# admin.site.register(Subcategory,SubcategoryAdmin)
# admin.site.register(Brand,BrandAdmin)
# admin.site.register(Product,ProductAdmin)
