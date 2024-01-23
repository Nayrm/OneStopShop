from django import forms
from .models import Benchstock_part, Benchstock_part_in_DC, Vendors, DC, Color, Furniture, Parts, SlatInformation, InventoryTransfer
from django.core.exceptions import ValidationError



class VendorsForm(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = ['vendor_name', 'vendor_id', 'vendor_code', 'sends_parts', 'available_parts', 'unavailable_parts', 'part_shipping', 'other_part_info']

class EditVendorForm(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = ['sends_parts', 'available_parts', 'unavailable_parts', 'part_shipping', 'other_part_info']

class DCForm(forms.ModelForm):
    class Meta:
        model = DC
        fields = ['dc_name', 'dc_number', 'rack_amount', 'shelf_per_rack']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['color_options']

class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = ['furniture_categories'] 

class PartsForm(forms.ModelForm):
    class Meta:
        model = Parts
        fields = ['part_categories']

class BenchstockPartForm(forms.ModelForm):
    class Meta:
        model = Benchstock_part
        fields = ['vendor', 'furniture_type', 'part_type', 'part_description', 'part_color', 'part_image']
        # Exclude 'discontinued' from widgets as well since it's no longer a field in the form
        widgets = {
            'vendor': forms.Select(),
            'furniture_type': forms.CheckboxSelectMultiple(),
            'part_type': forms.Select(),
            'part_description': forms.TextInput(),
            'part_color': forms.Select(),
            'part_image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(BenchstockPartForm, self).__init__(*args, **kwargs)
        self.fields['part_image'].required = False

class BenchstockDCPartForm(forms.ModelForm):
    class Meta:
        model = Benchstock_part_in_DC
        fields = ['dc','benchstock_part','quantity','optimal_quantity','rack_number','shelf_number','shelf_side']

class EditBenchstockPartInDCForm(forms.ModelForm):
    class Meta:
        model = Benchstock_part_in_DC
        fields = ['quantity', 'optimal_quantity', 'rack_number', 'shelf_number', 'shelf_side']


class SlatInformationForm(forms.ModelForm):
    class Meta:
        model = SlatInformation
        fields = ['vendor', 'sku', 'slat_amount', 'slat_length','center_slat_amount','center_slat_length','support_amount','support_height','mid_support_amount','mid_support_height']
       

class InventoryTransferForm(forms.ModelForm):
    class Meta:
        model = InventoryTransfer
        fields = ['to_dc', 'benchstock_part_in_dc', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        benchstock_part_in_dc = cleaned_data.get('benchstock_part_in_dc')
        quantity = cleaned_data.get('quantity')
        if benchstock_part_in_dc and quantity:
            if benchstock_part_in_dc.quantity < quantity:
                raise ValidationError({
                    'quantity': 'Insufficient quantity in source DC for transfer.'
                })

        return cleaned_data
    

