from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


DRAFT = ((0, "Yes"), (1, "No"))
FOR_SALE =((0, "For Sale"),(1, "Sold Out"))
CATEGORY =((0, "None"),(1, "Collars"),(2, "Leads"),(3, "Clothes"),(4, "Dog Treats"), (5, "Dog Food"),(6, "Dog Bowls"))

class Product(models.Model):
    '''
    Stores a single product
    '''
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.IntegerField(choices=CATEGORY, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    sold = models.IntegerField(choices=FOR_SALE, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    draft = models.IntegerField(choices=DRAFT, default=0)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"Product: {self.name}"

    

RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="product_reviews"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    ratings = models.IntegerField(choices=RATING, default=3)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Review | {self.content} by {self.author}"
    


class Order(models.Model):
    '''
    Creates and stores an order related to :modle: `store.Customer`
    '''
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


