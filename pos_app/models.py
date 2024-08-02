from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=200)
    unit_qty = models.IntegerField()
    qty_in_ltr = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Counter(models.Model):
    name = models.CharField(max_length=100)
    local_ip = models.CharField(max_length=15, unique=True)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=20, decimal_places=2)
    counter = models.ForeignKey(Counter,on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.DO_NOTHING)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields if needed
