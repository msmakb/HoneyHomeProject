from django.contrib import admin
from .models import *


class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'arrival_date', 
                    'quantity', 'description')

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'weight', 'is_retail')

class StockAdmin(admin.ModelAdmin):
    list_display = ('id',)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')

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

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'directory', 'name')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'name', 'gender', 
                    'nationality', 'date_of_birth', 
                    'address', 'contacting_email',
                    'phone_number', 'register_date')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'password', 'email')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'account', 'position')

class DistributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'account', 'stock')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'name', 'description', 
                    'status', 'receiving_date', 'deadline_date', 
                    'submission_date')

class TaskRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'on_time_rate', 'rate')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'week_start_date', 'week_end_date')

class WeeklyRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'rate')

# Register your models here.
admin.site.register(Batch, BatchAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(ItemCard, ItemCardAdmin)
admin.site.register(GoodsMovement, GoodsMovementAdmin)
admin.site.register(RetailCard, RetailCardAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskRate, TaskRateAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(WeeklyRate, WeeklyRateAdmin)
admin.site.register(RetailItem, RetailItemAdmin)
