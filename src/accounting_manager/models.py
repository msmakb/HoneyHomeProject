from statistics import mode
from django.db import models
from main.models import Distributor, ItemType, Batch

# Create your models here.
class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.IntegerField()
    date = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=255, default='-', null=True, blank=True)

    def __str__(self) -> str:
        return self.item

    def total(self):
        return self.quantity * self.price

class PricingRequest(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField(null=True, blank=True)

class Sales(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    date = models.DateField()
    seller = models.CharField(max_length=50, null=True, blank=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return self.type.name

    def getTotal(self):
        return self.quantity * self.price

