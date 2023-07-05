from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    season = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='product_images')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenProduct(Product):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.gender = 'M'
        super().save(*args, **kwargs)


class WomenProduct(Product):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.gender = 'F'
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Showing cart for: {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} ({self.quantity}) have been added"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.IntegerField(default=int(timezone.now().timestamp()))
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=100, null=True)
    shipping_method = models.CharField(max_length=255)
    shipping_address = models.TextField(max_length=100, null=True)
    phone = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"

    def calculate_total_amount(self):
        total = 0
        cart_items = self.cart.items.all()
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        return total
