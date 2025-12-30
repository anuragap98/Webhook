from django.db import models


class Order(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, default="pending")
    items = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.external_id} - {self.status}"


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    external_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20)
    method = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.external_id} for Order {self.order.external_id}"
