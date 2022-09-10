from django.contrib import admin
from .models import SalesHistory


class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'distributor', 'type', 'batch', 
                    'quantity', 'price', 'receiving_date', 
                    'received_from', 'payment_date')
                    
# Register your models here.
admin.site.register(SalesHistory, SalesHistoryAdmin)