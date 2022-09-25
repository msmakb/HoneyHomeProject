from django.contrib.auth.models import User, Group
from main.models import Person
from warehouse_admin.models import Stock
from .models import TaskRate


def onAddingNewEmployee(sender, instance, created, **kwargs):
    """
    This function called every time a new employee added.
    It creates a user account and assigns the person object to the employee.
    """
    if created:
        person = Person.objects.all().order_by('-id')[0]
        # Create new user
        User.objects.create_user(username=str(person.name).split(' ')[0],
                                email=person.contacting_email,
                                password=str(person.name).split(' ')[0],
                                first_name=str(person.name).split(' ')[0],
                                last_name=str(person.name).split(' ')[-1],
                                ).save()
        account = User.objects.all().order_by('-id')[0]
        # The position of the Employee
        Group.objects.get(name=instance.position).user_set.add(account)
        instance.account = account
        instance.person = person
        instance.save()

def onAddingNewDistributor(sender, instance, created, **kwargs):
    """
    This function called every time a new distributor added.
    It creates a user account, assigns the person object to the distributor, 
    and creates a new stock object to the distributor. 
    """
    if created:
        person = Person.objects.all().order_by('-id')[0]
        # Create new user for the distributor
        User.objects.create_user(username=str(person.name).split(' ')[0],
                                email=person.contacting_email,
                                password=str(person.name).split(' ')[0],
                                first_name=str(person.name).split(' ')[0],
                                last_name=str(person.name).split(' ')[-1],
                                ).save()
        account = User.objects.all().order_by('-id')[0]
        # Setting the distributor groupe
        Group.objects.get(name="Distributor").user_set.add(account)
        # Create new stock object for the distributor
        Stock.objects.create()
        stock = Stock.objects.all().order_by('-id')[0]
        # Assigning the objects to the distributor 
        instance.account = account
        instance.person = person
        instance.stock = stock
        instance.save()

def deleteUserAccount(sender, instance, using, **kwargs):
    """
    Delete the employee/distributor user account before the employee object
    """
    instance.account.delete()

def deleteTaskRate(sender, instance, using, **kwargs):
    """
    Delete the task rate before the task object getting deleted
    """
    try:
        task_rate = TaskRate.objects.get(task=instance)
        task_rate.delete()
    except TaskRate.DoesNotExist: pass
