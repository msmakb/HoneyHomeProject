from atexit import register
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


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

class Price(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return str(self.price)

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
    price = models.OneToOneField(Price, on_delete=models.SET_NULL, null=True, blank=True)
    receiving_date = models.DateField(auto_now_add=True)
    received_from = models.CharField(max_length=50)
    is_transforming = models.BooleanField(default=False, null=True, blank=True)
    is_priced = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.type.name}-{self.batch.name}'

    def getDistributor(self):
        return Distributor.objects.get(stock=self.stock)

    def getReceiver(self) -> str:
        if self.stock.id == 1:
            return "Main Storage"
        else:
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
    price = models.OneToOneField(Price, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.type.name}-{self.type.weight}'

class GoodsMovement(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemCard, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50, null=True, blank=True)
    receiver = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    directory = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)

class Person(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    COUNTRY = [
        ('YEM', 'YEMEN'),
        ('ID', 'INDONESIA')
    ]

    id = models.AutoField(primary_key=True)
    photo = models.OneToOneField(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,choices=GENDER, null=True, blank=True)
    nationality = models.CharField(max_length=10,choices=COUNTRY, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contacting_email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length= 50)

class Employee(models.Model):
    POSITIONS = [
        ('CEO', 'CEO'),
        ('Human Resources', 'Human Resources'),
        ('Warehouse Admin', 'Warehouse Admin'),
        ('Accounting Manager', 'Accounting Manager'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Designer', 'Designer'),
        ('Distributor', 'Distributor')
    ]

    id = models.AutoField(primary_key=True)
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=20, choices=POSITIONS)

    def __str__(self) -> str:
        return self.person.name

class Distributor(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.OneToOneField(Stock, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.person.name

class Task(models.Model):
    STATUS = [
        ('In-Progress','In-Progress'),
        ('On-Time','On-Time'),
        ('Late-Submission','Late-Submission'),
        ('Deadlined','Deadlined')
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    receiving_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    is_rated = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class TaskRate(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    on_time_rate = models.FloatField()
    rate = models.FloatField()

    def __str__(self) -> str:
        return str(self.rate)

class Week(models.Model):
    id = models.AutoField(primary_key=True)
    week_start_date = models.DateField(null=True, blank=True)
    week_end_date = models.DateField(null=True, blank=True)
    is_rated = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f'Week {self.id}' 

class WeeklyRate(models.Model):
    id = models.AutoField(primary_key=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.FloatField()

    def __str__(self) -> str:
        return str(self.rate)

