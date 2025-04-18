from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name} - PHP {self.price}'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.quantity} of {self.product} (User: {self.user.username})'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField()
    def __str__(self):
        return f'{self.user} - {self.created_at}'

class LineItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.transaction} - {self.product} x {self.quantity}'