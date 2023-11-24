from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

from django.db import models
from django.db.models.deletion import CASCADE

from main_app.custom_manager import ProfileManager
from main_app.mixins import TimestampedModel


class Profile(TimestampedModel):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(TimestampedModel):
    profile = models.ForeignKey('Profile', on_delete=CASCADE, related_name='orders')
    products = models.ManyToManyField('Product')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.profile.full_name}"
