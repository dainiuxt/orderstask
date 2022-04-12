from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
     
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField('Date', null=True, blank=True)

    ORDER_STATUS = (
        ('e', 'Entered'),
        ('w', 'Waiting'),
        ('p', 'In progress'),
        ('c', 'Completed'),
        )

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='e',
        help_text='Status',
        )

    def __str__(self):
        return f"{self.user.first_name} order No.{self.id} on {self.date}."

    @property
    def suma(self):
        order_rows = ProductOrder.objects.filter(order_id=self.id)
        recipe = 0
        for row in order_rows:
            recipe += row.quantity * row.selection.price
        return round(recipe, 2)


class Product(models.Model):
    name = models.CharField('Product name', max_length=200)
    price = models.FloatField('Price')

    def __str__(self):
        return f"Item {self.name} costs € {self.price}"    

class ProductOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    selection = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField('Quantity')

    @property
    def row_suma(self):
        row_cost = self.quantity * self.selection.price
        return round(row_cost, 2) 

