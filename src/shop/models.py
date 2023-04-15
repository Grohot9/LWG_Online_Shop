from django.db import models

from core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(default="default.png", upload_to="media/covers/")
    categories = models.ManyToManyField("shop.Category", related_name="products")


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Cart(BaseModel):
    user = models.ForeignKey(
        "account.UserProfile", on_delete=models.CASCADE, related_name="cart"
    )
    products = models.ManyToManyField(
        "Product", through="CartItem", related_name="cart"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50)


class CartItem(BaseModel):
    product = models.ForeignKey(
        "shop.Product", on_delete=models.CASCADE, related_name="cart_item"
    )
    cart = models.ForeignKey(
        "shop.Cart", on_delete=models.CASCADE, related_name="cart_item"
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
