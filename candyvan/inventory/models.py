from django.db import models
from django.contrib.auth.models import AbstractUser


class CandyUser(AbstractUser):
    pass


class Item(models.Model):
    name = models.CharField(max_length=30, unique=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"<Item `{self.name}` ({self.id})>"

    def __repr__(self):
        return self.__str__()


class Sale(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CandyUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        time_str = self.time.strftime('%Y-%m-%d %H:%M:%S')
        return f"<Sale by {self.user.username} at {time_str} ({self.id})>"

    def __repr__(self):
        return self.__str__()


class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CandyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True)

    def __str__(self):
        time_str = self.time.strftime('%Y-%m-%d %H:%M:%S')
        return f"<Transaction ${self.amount} by {self.user.username} " \
               f"at {time_str} ({self.id})>"

    def __repr__(self):
        return self.__str__()


class Revenue(models.Model):
    date = models.DateField(auto_now_add=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        date_str = self.date.isoformat()
        return f"<Revenue ${self.revenue} at {date_str} ({self.id})>"

    def __repr__(self):
        return self.__str__()


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CandyUser, on_delete=models.CASCADE)
    action = models.TextField()

    def __str__(self):
        time_str = self.time.strftime('%Y-%m-%d %H:%M:%S')
        return f"<Log {self.id} by {self.user.username} " \
               f"at {time_str} ({self.id})>"

    def __repr__(self):
        return self.__str__()
