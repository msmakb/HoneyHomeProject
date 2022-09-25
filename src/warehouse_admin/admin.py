from django.contrib import admin
from .models import Batch, ItemType, ItemCard, RetailItem, RetailCard, Stock, GoodsMovement


class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'arrival_date', 
                    'quantity', 'description')

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'weight', 'is_retail')

class ItemCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'batch', 'stock',
                    'quantity', 'status', 'price',
                    'receiving_date', 'received_from',
                    'is_transforming', 'is_priced')

class GoodsMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'sender', 'receiver', 'date')

class RetailCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'conversion_date', 'weight')
    
class RetailItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'quantity', 'price')

class StockAdmin(admin.ModelAdmin):
    list_display = ('id',)

# Registering models in admen page
admin.site.register(Batch, BatchAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemCard, ItemCardAdmin)
admin.site.register(GoodsMovement, GoodsMovementAdmin)
admin.site.register(RetailCard, RetailCardAdmin)
admin.site.register(RetailItem, RetailItemAdmin)
admin.site.register(Stock, StockAdmin)
