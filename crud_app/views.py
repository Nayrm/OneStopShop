from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from .forms import BenchstockPartForm, BenchstockDCPartForm, EditBenchstockPartInDCForm, VendorsForm, EditVendorForm, DCForm, ColorForm, FurnitureForm, PartsForm, SlatInformationForm, InventoryTransferForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import DC, Color, Furniture, Parts, Benchstock_part, Benchstock_part_in_DC, Vendors, SlatInformation, Log, InventoryTransfer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Benchstock_part_in_DC
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
import os
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from django.utils import timezone

#this is the login page
def index(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('crud_app:one_stop_shop')
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
    return render(request, 'crud_app/index.html', {'form': form})



#logout function from Navbar
def logout_request(request):
    logout(request)   
    return render(request, 'crud_app/logout.html')

def new_part(request):
    if request.method == 'POST':
        form = BenchstockPartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = BenchstockPartForm()
            return render(request, 'crud_app/new_part.html', {
        'form': form,
        'success_message': 'Benchstock SKU has been saved successfully.'
    })
    else:
        form = BenchstockPartForm()
    return render(request, 'crud_app/new_part.html',{'form': form})

def dc_parts(request):
    if request.method == 'POST':
        form = BenchstockDCPartForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the form and get the instance
                saved_instance = form.save()
                # Print the primary key of the saved instance
                print("Saved instance PK:", saved_instance.pk)
                messages.success(request, f'Benchstock SKU has been saved in DC successfully. PK: {saved_instance.pk}')
                form = BenchstockDCPartForm()  # Reset the form
            except IntegrityError:
                messages.error(request, 'Part has already been added to DC')
        else:
            messages.error(request, 'Please correct invalid fields.')
    else:
        form = BenchstockDCPartForm()

    return render(request, 'crud_app/dc_parts.html', {'form': form})


def edit_dc_parts(request, pk):
    instance = get_object_or_404(Benchstock_part_in_DC, pk=pk)
    if request.method == 'POST':
        form = EditBenchstockPartInDCForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'The item has been updated successfully.')
            return redirect('crud_app:all_dc_skus')
    else:
        form = EditBenchstockPartInDCForm(instance=instance)
    
    return render(request, 'crud_app/edit_dc_parts.html', {'form': form})


def all_skus(request):
    benchstock_parts = Benchstock_part.objects.all().order_by('vendor')
    last_benchstock_part = benchstock_parts.last()
    return render(request, 'crud_app/all_skus.html',{'benchstock_parts':benchstock_parts,'last_benchstock_part':last_benchstock_part})


def all_dc_skus(request):
    benchstock_parts_in_dc = Benchstock_part_in_DC.objects.all().order_by('benchstock_part__vendor__vendor_name', 'dc__dc_number')
    dc_choices = DC.objects.values_list('dc_name', flat=True).distinct()
    vendor_choices = Vendors.objects.values_list('vendor_id', flat=True).distinct()
    # Add other choices as needed

    # Apply filters based on GET parameters
    dc_filter = request.GET.get('dc_filter')
    vendor_filter = request.GET.get('vendor_filter')
    # Other filters...

    if dc_filter:
        benchstock_parts_in_dc = benchstock_parts_in_dc.filter(dc__dc_name=dc_filter)
    if vendor_filter:
        benchstock_parts_in_dc = benchstock_parts_in_dc.filter(benchstock_part__vendor__vendor_id=vendor_filter)
    return render(request, 'crud_app/all_dc_skus.html',{'benchstock_parts_in_dc':benchstock_parts_in_dc, 'dc_choices':dc_choices, 'vendor_choices':vendor_choices})

def all_vendors(request):
    vendors = Vendors.objects.all().order_by('vendor_name')
    return render(request, 'crud_app/all_vendors.html',{'vendors':vendors})

def new_vendor(request):
    if request.method == 'POST':
        form = VendorsForm(request.POST, request.FILES)
        if form.is_valid():
            new_vendor = form.save()
            vendor_id = new_vendor.vendor_id
            form = VendorsForm()
            Log.objects.create(
            user=request.user,
            action="Added a new item",
            status="success",
            details=f"Created Vendor: {vendor_id}"  # Replace with actual item details
        )
            return render(request, 'crud_app/new_vendor.html', {
        'form': form,
        })

    else:
        form = VendorsForm()
    return render(request, 'crud_app/new_vendor.html',{'form': form})


def edit_vendors(request, pk):
    instance = get_object_or_404(Vendors, pk=pk)
    if request.method == 'POST':
        form = EditVendorForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'The vendor has been updated successfully.')
            return redirect('crud_app:all_vendors')
    else:
        form = EditVendorForm(instance=instance)
    
    return render(request, 'crud_app/edit_vendors.html', {'form': form})

#Where users can add modify settings and options for the DCs, furniture categories, part catergories etc...
def settings(request):
    dcs = DC.objects.all().order_by('dc_number')
    colors = Color.objects.all().order_by('color_options')
    furniture_categories = Furniture.objects.all().order_by('furniture_categories')
    part_categories = Parts.objects.all().order_by('part_categories')

    return render(request, 'crud_app/settings.html', {'dcs': dcs, 'colors':colors,'furniture_categories':furniture_categories,'part_categories':part_categories})

def new_dc(request):
    if request.method == 'POST':
        form = DCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = DCForm()
            return redirect('crud_app:settings')
    else:
        form = DCForm()
    return render(request, 'crud_app/new_dc.html',{'form': form})

def new_color(request):
    if request.method == 'POST':
        form = ColorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ColorForm()
            return redirect('crud_app:settings')
    else:
        form = ColorForm()
    return render(request, 'crud_app/new_color.html',{'form': form})

def new_furniture_type(request):
    if request.method == 'POST':
        form = FurnitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FurnitureForm()
            return redirect('crud_app:settings')
    else:
        form = FurnitureForm()
    return render(request, 'crud_app/new_furniture_type.html',{'form': form})

def new_part_type(request):
    if request.method == 'POST':
        form = PartsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = PartsForm()
            return redirect('crud_app:settings')
    else:
        form = PartsForm()
    return render(request, 'crud_app/new_part_type.html',{'form': form})

def new_slat(request):
    if request.method == 'POST':
        form = SlatInformationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = SlatInformationForm()
            return redirect('crud_app:all_slat_info')
        else:
            print(form.errors)
    else:
        form = SlatInformationForm()
    return render(request, 'crud_app/new_slat.html',{'form': form})

def all_slat_info(request):
    slat_info = SlatInformation.objects.all().order_by('vendor__vendor_name')
    return render(request, 'crud_app/all_slat_info.html',{'slat_info':slat_info})

def one_stop_shop(request):
    benchstock_parts_in_dc = Benchstock_part_in_DC.objects.all().order_by('benchstock_part__vendor__vendor_name', 'dc__dc_number')
    slat_info = SlatInformation.objects.all().order_by('vendor__vendor_name')
    vendors = Vendors.objects.all().order_by('vendor_name')
    
    dc_choices = DC.objects.values_list('dc_name', flat=True).distinct()
    vendor_choices = Vendors.objects.values_list('vendor_id', flat=True).distinct()

    dc_filter = request.GET.get('dc_filter')
    vendor_filter = request.GET.get('vendor_filter')
    sku_filter = request.GET.get('sku_filter')

    if dc_filter:
        benchstock_parts_in_dc = benchstock_parts_in_dc.filter(dc__dc_name=dc_filter)
    if vendor_filter:
        slat_info = slat_info.filter(vendor__vendor_id=vendor_filter)
        vendors = vendors.filter(vendor_id=vendor_filter)
        benchstock_parts_in_dc = benchstock_parts_in_dc.filter(benchstock_part__vendor__vendor_id=vendor_filter)
    if sku_filter:
        slat_info = slat_info.filter(sku__icontains=sku_filter)
    return render(request, 'crud_app/one_stop_shop.html',{'benchstock_parts_in_dc':benchstock_parts_in_dc, 'dc_choices':dc_choices, 'vendor_choices':vendor_choices, 'slat_info':slat_info, 'vendors':vendors})

def generate_label(request, pk):
    benchstock_part = Benchstock_part_in_DC.objects.get(pk=pk)

    font_path = 'D:/programming_stuff/Django_CRUD/crud_app/static/crud_app/fonts/LibreBarcode39-Regular.ttf'
    pdfmetrics.registerFont(TTFont('LibreBarcode39', font_path))
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="part_label.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # Specify the exact coordinates for your label.
    p.rect(2, 660, 300, 130, stroke=1, fill=0)  # Change these values as needed
    p.drawString(22, 770, f"Vendor : {benchstock_part.benchstock_part.vendor.vendor_id} - {benchstock_part.benchstock_part.vendor.vendor_name} ")
    p.drawString(22, 755, f"BS.SKU: {benchstock_part.benchstock_part.benchstock_sku} - DC# {benchstock_part.dc.dc_number}")
    p.drawString(22, 740, f"Location:  Rack #{benchstock_part.rack_number} - Shelf #{benchstock_part.shelf_number} - Shelf side: {benchstock_part.shelf_side}")
    p.drawString(22, 725, f"Optimal Quantity: {benchstock_part.optimal_quantity}")

    p.setFont("LibreBarcode39", 50)
    p.drawString(22, 680, f"*{benchstock_part.benchstock_part.benchstock_sku}*")
    # Add more details as needed

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Return the response
    return response

def new_inventory_transfer(request):
    if request.method == 'POST':
        form = InventoryTransferForm(request.POST, request.FILES)
        if form.is_valid():
            inventory_transfer = form.save()
            
            # Subtract quantity from benchstock_part_in_dc
            benchstock_part_in_dc = inventory_transfer.benchstock_part_in_dc
            benchstock_part_in_dc.quantity -= inventory_transfer.quantity
            benchstock_part_in_dc.save()

            # Generate PDF
            buffer = BytesIO()
            font_path = 'D:/programming_stuff/Django_CRUD/crud_app/static/crud_app/fonts/LibreBarcode39-Regular.ttf'
            pdfmetrics.registerFont(TTFont('LibreBarcode39', font_path))
            p = canvas.Canvas(buffer, pagesize=letter)
            # Add your PDF content here
            p.drawString(100, 770, "Benchstock Transfer Label")
            p.drawString(100, 750, f"Transfer Number: {inventory_transfer.transfer_number}")
            p.drawString(100, 735, f"From DC: {inventory_transfer.benchstock_part_in_dc.dc}")
            p.drawString(100, 720, f"To DC: {inventory_transfer.to_dc}")
            p.drawString(100, 705, f"SKU: {inventory_transfer.benchstock_part_in_dc.benchstock_part.benchstock_sku}")
            p.drawString(100, 690, f"Quantity: {inventory_transfer.quantity}")
            

            p.setFont("LibreBarcode39", 50)
            p.drawString(100, 630, f"*{inventory_transfer.transfer_number}*")

            # ... more content
            p.showPage()
            p.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="transfer_{inventory_transfer.transfer_number}.pdf"'
            return response

    else:
        form = InventoryTransferForm()

    return render(request, 'crud_app/new_inventory_transfer.html', {'form': form})

def receive_inventory_transfer(request):
    return render(request, 'crud_app/receive_inventory_transfer.html')

def process_transfer(request):
    if request.method == 'POST':
        transfer_number = request.POST.get('transfer_number')
        transfer = get_object_or_404(InventoryTransfer, pk=transfer_number)
        new_record_created = False

        if transfer.status != 'Received':
            try:
                receiving_dc_record = Benchstock_part_in_DC.objects.get(
                    dc=transfer.to_dc,
                    benchstock_part=transfer.benchstock_part_in_dc.benchstock_part
                )
            except Benchstock_part_in_DC.DoesNotExist:
                receiving_dc_record = Benchstock_part_in_DC.objects.create(
                    dc=transfer.to_dc,
                    benchstock_part=transfer.benchstock_part_in_dc.benchstock_part,
                    quantity=0,
                    rack_number=0,
                    shelf_number=0,
                    shelf_side='A',
                    optimal_quantity=10
                )
                new_record_created = True

            receiving_dc_record.quantity += transfer.quantity
            receiving_dc_record.save()

            # Update transfer record
            transfer.status = 'Received'
            transfer.received_date = timezone.now()
            transfer.save()

            if new_record_created:
                # Redirect to the edit page of the newly created object
                edit_url = reverse('crud_app:edit_dc_parts', kwargs={'pk': receiving_dc_record.pk})
                return redirect(edit_url)

            messages.success(request, f"Transfer {transfer_number} has been processed successfully.")
            return redirect('crud_app:all_dc_skus')  # Redirect to a success page or any other page
        else:
            messages.error(request, f"Transfer {transfer_number} has already been processed.")
            return redirect('crud_app:receive_inventory_transfer')
    else:
        return render(request, 'crud_app/receive_inventory_transfer.html')
    

    
def process_quick_scan(request):
    if request.method == 'POST':
        dc_id = request.POST.get('dc')
        sku = request.POST.get('sku')

        try:
            dc = DC.objects.get(pk=dc_id)
            benchstock_part = Benchstock_part_in_DC.objects.get(benchstock_part__benchstock_sku=sku, dc=dc)

            if benchstock_part.quantity > 0:
                benchstock_part.quantity -= 1
                benchstock_part.save()
                messages.success(request, 'Quantity updated successfully.')
            else:
                messages.error(request, 'No stock available to decrement.')

        except DC.DoesNotExist:
            messages.error(request, 'Selected DC does not exist.')
        except Benchstock_part_in_DC.DoesNotExist:
            messages.error(request, 'SKU not found in selected DC.')

        return redirect('crud_app:process_quick_scan')  # Replace with your template name or URL name

    else:
        dcs = DC.objects.all()
        return render(request, 'crud_app/quick_scan.html', {'dcs': dcs})