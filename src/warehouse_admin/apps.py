from django.apps import AppConfig
from django.db.models.signals import post_migrate


class WarehouseAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warehouse_admin'

    def ready(self) -> None:
        from .signals import onMigratingStockModel

        post_migrate.connect(onMigratingStockModel, sender=self)

        return super().ready()
