from django.contrib import admin
from core.models import Product, Category, Order, OrderItem, Cart, SubCategory, Person

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(SubCategory)
admin.site.register(Person)