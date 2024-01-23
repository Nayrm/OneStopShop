from django.contrib import admin
from .models import Vendors, DC, Parts, Furniture, Color, Benchstock_part, Benchstock_part_in_DC, SlatInformation, Log, InventoryTransfer
# Register your models here.
admin.site.register(Vendors)
admin.site.register(DC)
admin.site.register(Parts)
admin.site.register(Furniture)
admin.site.register(Color)
admin.site.register(Benchstock_part)
admin.site.register(Benchstock_part_in_DC)
admin.site.register(SlatInformation)
admin.site.register(InventoryTransfer)
admin.site.register(Log)

