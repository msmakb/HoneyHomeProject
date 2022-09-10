from django.db import models
from main.models import ItemType, Batch, Price, Distributor

# Create your models here.
class SalesHistory(models.Model):
    id = models.AutoField(primary_key=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    receiving_date = models.DateField(null=True, blank=True)
    received_from = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateField(auto_now_add=True)

    def getTotal(self):
        return self.price * self.quantity