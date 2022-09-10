from django.shortcuts import render
from accounting_manager.models import Sales
from main.models import GoodsMovement

# Create your views here.
def Dashboard(request):
    sales = Sales.objects.filter(is_approved=True).order_by('-id')[:5]
    goodsMovement = GoodsMovement.objects.all().order_by('-id')[:3]
    context = {'GoodsMovement':goodsMovement, 'Sales':sales}
    return render(request, 'ceo/dashboard.html', context)