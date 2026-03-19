from django.db import models

# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
        CATEGORY_CHOICE=(('fruits','fruits'),
                         ('vegitable','vegitable'))
        img=models.ImageField(upload_to="shop")
        name=models.CharField(max_length=50)
        description=models.CharField(max_length=50)
        price=models.IntegerField()
        category = models.CharField(max_length=20, choices=CATEGORY_CHOICE, default='fruits')

        def  __str__(self):
            return self.name
    
class Checkout(models.Model):
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)
    company_name=models.CharField(max_length=100,blank=True,null=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    pin_code=models.IntegerField(blank=True,null=True)
    mobile=models.IntegerField(blank=True,null=True)
    email=models.EmailField()
    create_an_account=models.BooleanField(default=False,blank=True,null=True)
    different_address=models.CharField(max_length=200,blank=True,null=True)
    notes=models.CharField(max_length=200,blank=True,null=True)
    
    def __str__(self):
        return self.first_name
    
    
class Cart(models.Model):
    session_key = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
class OrderItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price=models.FloatField()

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    
class Order(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    order_notes = models.TextField(blank=True, null=True)
    create_account = models.BooleanField(default=False)
    ship_different = models.BooleanField(default=False)
    country=models.CharField(max_length=100)
    
    def __str__(self):
        return f"Order {self.id} - {self.name}"
    
    
    


    

 
    