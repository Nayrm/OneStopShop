from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
# Create your models here.



class Vendors(models.Model):
    vendor_name = models.CharField(max_length=100 ,unique=True)
    vendor_id = models.CharField(max_length=4 ,unique=True)
    vendor_code = models.PositiveSmallIntegerField(unique=True)
    SEND_PART_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    sends_parts = models.CharField(choices=SEND_PART_CHOICES, max_length=3, default='Yes')
    available_parts = models.CharField(max_length=500, blank=True)
    unavailable_parts = models.CharField(max_length=500, blank=True)
    part_shipping = models.CharField(max_length=400, blank=True)
    other_part_info = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.vendor_name} - {self.vendor_id}"
    
    def vendor_code_only(self):
        return f"{self.vendor_code}"
    
    def benchstock_items_count(self):
        return Benchstock_part.objects.filter(vendor=self).count()
    

class Furniture(models.Model):
    furniture_categories = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"{self.furniture_categories}"
    

class Parts(models.Model):
    part_categories = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"{self.part_categories}"
    
class Color(models.Model):
    color_options = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return f"{self.color_options}"


class DC(models.Model):
    dc_name = models.CharField(max_length=80, unique=True)
    dc_number = models.PositiveSmallIntegerField(unique=True)
    rack_amount = models.SmallIntegerField()
    shelf_per_rack = models.SmallIntegerField()
    def __str__(self):
        return f"{self.dc_name} - {self.dc_number}" 
    

class Benchstock_part(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True)
    benchstock_sku = models.PositiveIntegerField(unique=True, editable=False)
    furniture_type = models.ManyToManyField(Furniture)
    part_type = models.ForeignKey(Parts, on_delete=models.SET_NULL, null=True)
    part_description = models.CharField(max_length=50, blank=True)
    part_color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    part_image = models.ImageField(null=True, storage=DefaultStorage())
    ACTIVE_CHOICES =  [
        ('Active', 'Active'),
        ('Discontinued', 'Discontinued'),
    ]
    discontinued = models.CharField(choices=ACTIVE_CHOICES, max_length=30, default='Active')

    class Meta:
        unique_together = [['vendor','part_type','part_description','part_color']]

    def save(self, *args, **kwargs):
        if not self.pk:
            count = Benchstock_part.objects.filter(vendor=self.vendor).count() + 1
            self.benchstock_sku = int(f"{self.vendor.vendor_code}0850{count:02d}")
        super(Benchstock_part, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor} - {self.benchstock_sku} - {self.part_color} - {self.part_type}"


class Benchstock_part_in_DC(models.Model):
    dc = models.ForeignKey(DC, on_delete=models.CASCADE)
    benchstock_part = models.ForeignKey(Benchstock_part, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    optimal_quantity = models.PositiveSmallIntegerField()
    rack_number = models.PositiveSmallIntegerField()
    shelf_number = models.PositiveSmallIntegerField()
    SELF_SIDE_CHOICES = [
        ('A','A'),
        ('B','B'),
    ]
    shelf_side = models.CharField(choices=SELF_SIDE_CHOICES, max_length=1)

    class Meta:
        unique_together = [['dc', 'benchstock_part']]
    
    def clean(self):
        if self.rack_number > self.dc.rack_amount:
            raise ValidationError({'rack_number': 'Rack Number is invalid, exceeds rack limit for DC'})
        if self.shelf_number > self.dc.shelf_per_rack:
            raise ValidationError({'shelf_number': 'Shelf Number is invalid, exceeds shelf limit for DC'})
        
    def __str__(self):
            return f"DC: {self.dc} SKU: {self.benchstock_part.benchstock_sku} Quantity: {self.quantity}"
    
class SlatInformation(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True)
    sku = models.PositiveIntegerField(unique=True)
    slat_amount = models.PositiveIntegerField(blank=True, null=True)
    slat_length = models.PositiveIntegerField(blank=True, null=True)
    center_slat_amount = models.PositiveIntegerField(blank=True, null=True)
    center_slat_length = models.PositiveIntegerField(blank=True, null=True)
    support_amount = models.PositiveIntegerField(blank=True, null=True)
    support_height = models.PositiveIntegerField(blank=True, null=True)
    mid_support_amount = models.PositiveIntegerField(blank=True, null=True)
    mid_support_height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.vendor} - {self.sku}"
    

class InventoryTransfer(models.Model):
    transfer_number = models.AutoField(primary_key=True)
    to_dc = models.ForeignKey(DC, on_delete=models.CASCADE, related_name='to_dc')
    benchstock_part_in_dc = models.ForeignKey(Benchstock_part_in_DC, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    shipping_date = models.DateField(auto_now_add=True)
    received_date = models.DateField(blank=True, null=True)
    STATUS_CHOICES = [
        ('Lost', 'Lost'),
        ('Shipped', 'Shipped'),
        ('Received', 'Received'),
    ]
    status = models.CharField(max_length=30, default='Shipped', choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.transfer_number} - {self.benchstock_part_in_dc} - {self.quantity}"
    
    def clean(self):
        if self.benchstock_part_in_dc.dc == self.to_dc:
            raise ValidationError("From and To DC cannot be the same.")

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    details = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.date_time} - {self.action} - {self.status}"
    

