from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from ..common.models import BaseModel
from ..store.models.product import Product
from ..store.models.variants import ProductVariants

# Account
User = get_user_model()


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"{self.user}"


class StatusChoices(models.TextChoices):
    # TODO Move to common
    ACTIVE = "active"
    INACTIVE = "inactive"


# Product item in cart
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    variations = models.ManyToManyField(ProductVariants, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.product}"

    @property
    def get_price(self):
        print(self.product.discount if self.product.discount else self.product.price)
        return self.product.discount if self.product.discount else self.product.price
