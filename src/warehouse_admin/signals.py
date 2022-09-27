from .models import Stock

def onMigratingStockModel(**kwargs):
    """
    Creating the main storage stock.
    """
    if not Stock.objects.all().exists():
        Stock.objects.create()
        print('  Main storage stock created')
