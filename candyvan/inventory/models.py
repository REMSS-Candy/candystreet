from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    permission = models.IntegerField(default=99)


class Item(models.Model):
    name = models.CharField(30, unique=True)
    buy_price = models.IntegerField()
    sell_price = models.IntegerField()
    quantity = models.IntegerField(default=0)


class Sale(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True)


class Revenue(models.Model):
    date = models.DateField(auto_now_add=True)
    revenue = models.IntegerField(default=0)


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
