from django.shortcuts import redirect, render
from django.contrib import messages
from distributor.models import Distributor
from main.decorators import allowed_users
from main.tasks import getEmployeesTasks
from main.utils import getUserBaseTemplate as base
from .models import (ItemCard, RetailCard, Stock, ItemType, Batch,
                         GoodsMovement, RetailItem)
from .forms import (AddGoodsForm, RegisterItemForm, AddBatchForm, 
                    SendGoodsForm, AddRetailGoodsForm, ConvertToRetailForm)


# Create your views here.
# ----------------------------Dashboard------------------------------
@allowed_users(allowed_roles=['Admin', 'Warehouse Admin'])
def warehouseAdminDashboard(request):
    goodsMovement = GoodsMovement.objects.all().order_by('-id')[:3]
    context = {'GoodsMovement':goodsMovement, 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/dashboard.html', context)
# --------------------------Main Storage-----------------------------
def MainStorageGoodsPage(request):
    MainStorageStock = Stock.objects.filter(id=1)[0]
    Items = ItemCard.objects.filter(stock=MainStorageStock, status='Good', is_transforming=False).order_by('type')
    context = {'Items':Items, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/main_storage_goods.html', context)

def AddGoodsPage(request):
    form = AddGoodsForm()
    MainStorageStock = Stock.objects.filter(id=1)[0]
    if request.method == "POST":
        form = AddGoodsForm(request.POST)
        if form.is_valid:
            type = form['type'].value()
            batch = form['batch'].value()
            quantity = form['quantity'].value()
            received_from = form['received_from'].value()
            ItemCard.objects.create(type=ItemType.objects.get(id=type),
                                    batch=Batch.objects.get(id=batch),
                                    stock=MainStorageStock,
                                    quantity=quantity,
                                    status='Good',
                                    received_from=received_from)
        return redirect('MainStorageGoodsPage')

    context = {'form':form, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/add_goods.html', context)

# --------------------------Registered Items--------------------------
def RegisteredItemsPage(request):
    Items= ItemType.objects.all()
    context = {'Items':Items, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/registered_items.html', context)

def RegisterItemPage(request):
    form = RegisterItemForm()
    if request.method == "POST":
        form = RegisterItemForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('RegisteredItemsPage')
    context = {'form':form, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/register_item.html', context)   
# -------------------------------Batches-------------------------------
def BatchesPage(request):
    Batches = Batch.objects.all()
    context = {'Batches':Batches, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/batches.html', context)

def AddBatchPage(request):
    form = AddBatchForm()
    if request.method == "POST":
        form = AddBatchForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('BatchesPage')
    context = {'form':form, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/add_batch.html', context)
# --------------------------Distributed Goods---------------------------
def DistributedGoodsPage(request):
    Distributors = {}
    MainStorageStock = Stock.objects.filter(id=1)[0]
    Stocks = Stock.objects.all()
    for stock in Stocks:
        if stock == MainStorageStock:
            continue
        quantityOfGoods = 0
        distributor = Distributor.objects.get(stock=stock)
        distributorStock = ItemCard.objects.filter(stock=stock)
        for stock in distributorStock:
            quantityOfGoods += stock.quantity
        Distributors[distributor.id] = {'distributor': distributor,
                                        'quantityOfGoods':quantityOfGoods}

    context = {'Distributors':Distributors, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/distributed_goods.html', context)

def DistributorStockPage(request, pk):
    distributor = Distributor.objects.get(id=pk)
    Items = ItemCard.objects.filter(stock=distributor.stock).order_by('type')
    context = {'distributor':distributor, 'Items':Items, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/distributor_stock.html', context)

def SendGoodsPage(request, pk):
    form = SendGoodsForm(1)
    distributor = Distributor.objects.get(id=pk)
    stock = distributor.stock
    availableItems= {}
    Items = ItemCard.objects.filter(stock=1, status='Good')
    for i in Items:
        availableItems[i.id] = {'name':i.type, 'batch':i.batch, 'quantity':i.quantity}
    if request.method == "POST":
        form = SendGoodsForm(1, request.POST)
        if form.is_valid:
            name = form['type'].value()
            batch = form['batch'].value()
            quantity = form['quantity'].value()
            received_from = form['received_from'].value()
            is_available = False
            for key, value in availableItems.items():
                if str(value['name']) == name and str(value['batch']) == batch and int(value['quantity']) >= int(quantity):
                    name = ItemType.objects.get(name=str(value['name']))
                    batch = Batch.objects.get(name=str(value['batch']))
                    is_available = True
                    if int(value['quantity']) == int(quantity):
                        ItemCard.objects.get(type=name, batch=batch, stock=1, quantity=int(quantity)).delete()
                    else: 
                        q = ItemCard.objects.filter(type=name, batch=batch, stock=1)[0]
                        q.quantity = int(q.quantity - int(quantity))
                        q.save()

            if is_available:  
                ItemCard.objects.create(type=ItemType.objects.get(name=name),
                                        batch=Batch.objects.get(name=str(batch)),
                                        stock=stock,
                                        quantity=quantity,
                                        status='Good',
                                        received_from="Main Storage",
                                        is_transforming=True)
                GoodsMovement.objects.create(item=ItemCard.objects.all().order_by('-id')[0],
                                            sender='Main Storage',
                                            receiver=str(distributor.person.name))
            else:
                messages.info(request, "Item or quantity is not available in the stock")
                return redirect('SendGoodsPage', pk)
        return redirect('DistributorStockPage', pk)
    context = {'availableItems':availableItems, 'form':form, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/send_goods.html', context)

def GoodsMovementPage(request):
    goodsMovement = GoodsMovement.objects.all()
    context = {'GoodsMovement':goodsMovement, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/goods_movement.html', context)

def DamagedGoodsPage(request):
    MainStorageStock = Stock.objects.get(id=1)
    Items = ItemCard.objects.filter(stock=MainStorageStock, status='Damaged', is_transforming=False)
    context = {'Items':Items, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/damaged_goods.html', context)

def AddDamagedGoodsPage(request):
    MainStorageStock = Stock.objects.get(id=1)
    form = SendGoodsForm(1)
    availableItems= {}
    Items = ItemCard.objects.filter(stock=1, status='Good')
    for i in Items:
        availableItems[i.id] = {'name':i.type, 'batch':i.batch, 'quantity':i.quantity}
    if request.method == "POST":
        form = SendGoodsForm(1, request.POST)
        if form.is_valid:
            name = form['type'].value()
            batch = form['batch'].value()
            quantity = form['quantity'].value()
            received_from = form['received_from'].value()
            is_available = False
            for key, value in availableItems.items():
                if str(value['name']) == name and str(value['batch']) == batch and int(value['quantity']) >= int(quantity):
                    name = ItemType.objects.get(name=str(value['name']))
                    batch = Batch.objects.get(name=str(value['batch']))
                    is_available = True
                    if int(value['quantity']) == int(quantity):
                        ItemCard.objects.get(type=name, batch=batch, stock=1, quantity=int(quantity)).delete()
                    else: 
                        q = ItemCard.objects.get(type=name, batch=batch, stock=1) 
                        q.quantity = int(q.quantity - int(quantity))
                        q.save()

            if is_available:  
                ItemCard.objects.create(type=ItemType.objects.get(name=name),
                                        batch=Batch.objects.get(name=str(batch)),
                                        stock=MainStorageStock,
                                        quantity=quantity,
                                        status='Damaged',
                                        received_from=received_from)
            else:
                messages.info(request, "Item or quantity is not available in the stock")
                return redirect('AddDamagedGoodsPage')
        return redirect('DamagedGoodsPage')
    context = {'availableItems':availableItems, 'form':form, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/add_damaged_goods.html', context)

def TransformedGoodsPage(request):
    Items = ItemCard.objects.filter(is_transforming=True)
    
    context = {'Items':Items, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/transformed_goods.html', context)

def ApproveTransformedGoods(request, pk):
    item = ItemCard.objects.get(id=pk)
    item.is_transforming = False
    item.save()

    if not ItemCard.objects.filter(is_transforming=True).exists():
        messages.info(request, "There is no transformed goods to be approved") 
        from main.models import Task
        task = Task.objects.get(id=10)
        task.is_rated = True
        task.status = "On-Time"
        task.save()
    messages.success(request, f"The transformed goods '{item.type}' from '{item.received_from}' to '{item.getReceiver()}' has been 'approved'")
    return redirect(TransformedGoodsPage)

def RetailGoodsPage(request):
    retailCard = RetailCard.objects.all()
    retailItem = RetailItem.objects.all()
    context = {'retailItem':retailItem, 'retailCard':retailCard, 'base':base(request), 'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/retail_goods.html', context)

def ConvertToRetailPage(request):
    form = ConvertToRetailForm()
    availableItems= {}
    Items = ItemCard.objects.filter(stock=1, status="Good")
    for i in Items:
        availableItems[i.id] = {'name':i.type, 'batch':i.batch, 'quantity':i.quantity}
    if request.method == "POST":
        form = ConvertToRetailForm(request.POST)
        if form.is_valid:
            name = form['type'].value()
            batch = form['batch'].value()
            quantity = form['quantity'].value()
            is_available = False
            for key, value in availableItems.items():
                if str(value['name']) == name and str(value['batch']) == batch and int(value['quantity']) >= int(quantity):
                    name = ItemType.objects.get(name=str(value['name']))
                    batch = Batch.objects.get(name=str(value['batch']))
                    is_available = True
                    if int(value['quantity']) == int(quantity):
                        ItemCard.objects.get(type=name, batch=batch, status="Good", stock=1, quantity=int(quantity)).delete()
                    else: 
                        q = ItemCard.objects.get(type=name, batch=batch, status="Good", stock=1) 
                        q.quantity = int(q.quantity - int(quantity))
                        q.save()

            if is_available:  
                RetailCard.objects.create(type=ItemType.objects.get(name=name), weight=int(quantity) * 7000)
            else:
                messages.info(request, "Item or quantity is not available in the stock")
                return redirect('ConvertToRetailPage')
        return redirect('RetailGoodsPage')

    context = {'availableItems':availableItems, 'form':form, 'base':base(request),'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/convert_to_retail.html', context)

def AddRetailGoodsPage(request):
    form = AddRetailGoodsForm()
    if request.method == "POST":
        form = AddRetailGoodsForm(request.POST)
        if form.is_valid():
            stock = RetailItem.objects.all()
            name = form['type'].value()
            Type = ItemType.objects.get(name=str(name))
            quantity = form['quantity'].value()
            is_available = False
            for item in stock:
                if item.type == Type:
                    is_available = True
            if is_available:
                q = RetailItem.objects.get(type=Type)
                q.quantity = int(q.quantity + int(quantity))
                q.save()
            else:
                RetailItem.objects.create(type=Type, quantity=quantity)
            q = RetailCard.objects.all()[0]
            q.weight = int(q.weight) - int(RetailItem.objects.all().order_by('-id')[0].type.weight)
            q.save()
        return redirect('RetailGoodsPage')

    context = {'form':form, 'base':base(request),'getEmployeesTasks':getEmployeesTasks(request)}
    return render(request, 'warehouse_admin/add_retail_goods.html', context)
