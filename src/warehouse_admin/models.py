from django.db import models


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=30, null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    is_retail = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    

class ItemCard(models.Model):
    STATUS = [
        ('Good', 'Good'),
        ('Damaged', 'Damaged'),
        ('Frozen', 'Frozen'),
    ]
    
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, default='Good', choices=STATUS)
    price = models.IntegerField(null=True, blank=True)
    receiving_date = models.DateField(auto_now_add=True)
    received_from = models.CharField(max_length=50)
    is_transforming = models.BooleanField(default=False, null=True, blank=True)
    is_priced = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.type.name}-{self.batch.name}'

    def getDistributor(self):
        from distributor.models import Distributor
        
        return Distributor.objects.get(stock=self.stock)

    def getReceiver(self) -> str:
        if self.stock.id == 1:
            return "Main Storage"
        else:
            from distributor.models import Distributor

            return Distributor.objects.get(stock=self.stock).person.name

    def getTotal(self):
        return self.price.price * self.quantity

class RetailCard(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    conversion_date = models.DateField(auto_now_add=True)
    weight = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.type.name}'

class RetailItem(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.type.name}-{self.type.weight}'

class GoodsMovement(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemCard, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50, null=True, blank=True)
    receiver = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
