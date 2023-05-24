from django.db import models
from django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES=(
    ('AP','Apple'),
    ('LE','Lenovo'),
    ('HP','Hp'),
    ('DL','Dell'),
    ('Acer','Acer'),
    ('Toshiba','Toshiba'),
    ('Asus','Asus'),
    ('MS','Microsoft Laptop'),
)

STATE_CHOICES=(
    ('Eastern Region','Eastern Region'),
    ('Greater Accra','Greater Accra'),
    ('Ahafo Region','Ahafo Region'),
    ('Ashanti','Ashanti'),
    ('Bono East','Bono East'),
    ('Brong Ahafo','Brong Ahafo'),
    ('Central Region','Central Region'),
    ('North East','North East'),
    ('Northern','Northern'),
    ('Oti Region','Oti Region'),
    ('Savannah Region','Savannah Region'),
    ('Upper East','Upper East'),
    ('Upper West','Upper West'),
    ('Western Region','Western Region'),
    ('Western North','Western North'),
    ('Volta Region','Volta Region'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    about_the_device = models.TextField(default='')
    note = models.TextField(default='')
    product_in_stock = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image = models.ImageField(upload_to='product', default='default_image.jpg')
    
    def __str__(self):
        return self.title
    
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    phone = models.IntegerField(default=9999999999)
    zipcode = models.IntegerField(default=1234)
    region = models.CharField(choices=STATE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price 
    
STATUS_CHOICES=(
    ('Order Seen','Order Seen'),
    ('Packaging','Packaging'),
    ('On Delivering','On Delivering'),
    ('Order Cancelled','Order Cancelled'),
    ('Pending','Pending'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE, default="")
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    