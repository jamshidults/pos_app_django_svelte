from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=200)
    unit_qty = models.IntegerField()
    qty_in_ltr = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    # Add other fields if needed

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields if needed
