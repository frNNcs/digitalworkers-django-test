from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Contract(models.Model):
    start_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class RecurrentContract(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
