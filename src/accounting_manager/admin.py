from django.contrib import admin
from .models import Expenses, PricingRequest, Sales

class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'price', 'date', 'note')

class PricingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'batch', 'quantity', 'price', 'date', 'seller')

# Register your models here.
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(PricingRequest, PricingRequestAdmin)
admin.site.register(Sales, SalesAdmin)

