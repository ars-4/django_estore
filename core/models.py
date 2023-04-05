from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, default='customer')
    email = models.EmailField()
    # profile_image = models.ImageField(upload_to='profile_image', null=True)
    profile_image_url = models.CharField(max_length=255, null=True, default='')
    phone = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255, null=True)
    address_city = models.CharField(max_length=255, null=True)
    address_state = models.CharField(max_length=255, null=True)
    address_zip = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username
    


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255, null=True, default='0')
    description = models.TextField()
    color = models.CharField(max_length=255, null=True, default='white')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='product_image')
    image_url = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return self.name


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=244, null=True, default='0')
    price = models.CharField(max_length=244, null=True, default='0')
    total = models.CharField(max_length=244, null=True, default='0')

    def __str__(self):
        return self.product.name


class Cart(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    total = models.CharField(max_length=244, null=True, default='0')

    def __str__(self):
        return self.person.name
    

class Order(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.CharField(max_length=244, null=True, default='0')

    def __str__(self):
        return self.person.name
    