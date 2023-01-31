from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
# from django.db.models import Sum


class Account(AbstractUser):
    is_supporter = models.BooleanField(default=False)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        help_text=_("Required"),
        unique=True,
        null=False,
        blank=False,
    )
    state = models.CharField(
        verbose_name=_("State"),
        help_text=_("Required"),
        max_length=125,
    )
    city = models.CharField(
        verbose_name=_("City"),
        help_text=_("Required"),
        max_length=125,
    )
    address = models.CharField(
        verbose_name=_("Address"),
        help_text=_("Required"),
        max_length=255,
    )
    zip_code = models.CharField(
        max_length=100,
        verbose_name=_("Zip code"),
        help_text=_("Required"),
    )

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.get_full_name()


class Ticket(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user",
    )
    title = models.CharField(
        verbose_name=_("Ticket title"),
        help_text=_("Required and unique"),
        max_length=255,
        default=None,
    )
    user_text = models.TextField()
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )


class TicketAnswer(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )
    answer = models.TextField()

    def __str__(self):
        return f"{self.ticket.title} | {self.ticket.owner.__str__()}"


# class ShoppingCart(models.Model):
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="owner",
#     )
#     total = models.FloatField(
#         verbose_name=_("Total amount"),
#         null=True,
#         blank=True,
#     )
#     coupon = models.ForeignKey(
#         "Coupon",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#     )
#     created_at = models.DateTimeField(
#         _("Created at"),
#         auto_now_add=True,
#         editable=False,
#     )
#     is_paid = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = _("Shopping cart")
#         verbose_name_plural = _("Shopping carts")
#         ordering = ("created_at", "is_paid")
#
#     def save(self, *args, **kwargs):
#         items_price = CartItem.objects.filter(cart__id=self.id).aggregate(Sum("price"))
#         coupon = self.coupon
#         if items_price is not None:
#             if coupon is not None:
#                 if coupon.is_active:
#                     if items_price.get("price_sum"):
#                         self.total = items_price.get("price__sum") - coupon.discount_price
#                     else:
#                         self.total = 0
#             self.total = items_price.get("price__sum")
#         else:
#             self.total = 0
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.owner.__str__()} | {self.id}"


# class CartItem(models.Model):
#     cart = models.ForeignKey(
#         ShoppingCart,
#         on_delete=models.CASCADE,
#         related_name="cart_items",
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         default=None,
#     )
#     price = models.FloatField(
#         null=True,
#         blank=True,
#     )
#     quantity = models.IntegerField()
#
#     def save(self, *args, **kwargs):
#         self.price = int(self.product.discount_price * self.quantity)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.product.title


class Coupon(models.Model):
    title = models.CharField(
        verbose_name=_("Ticket title"),
        help_text=_("Required and unique"),
        max_length=255,
        default=None,
    )
    code = models.UUIDField(default=uuid4, unique=True)
    discount_price = models.IntegerField(
        verbose_name=_("Discount price"),
    )
    start_at = models.DateTimeField(
        _("Start at"),
        auto_now_add=True,
        editable=False,
    )
    end_at = models.DateTimeField(
        _("End at"),
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.title
