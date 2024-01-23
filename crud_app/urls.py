from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import edit_dc_parts

app_name = 'crud_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_request, name='logout'),
    path('settings', views.settings, name='settings'),
    path('new_dc', views.new_dc, name='new_dc'),
    path('new_color', views.new_color, name='new_color'),
    path('new_furniture_type', views.new_furniture_type, name='new_furniture_type'),
    path('new_part_type', views.new_part_type, name='new_part_type'),
    path('new_part', views.new_part, name='new_part'),
    path('dc_parts', views.dc_parts, name='dc_parts'),
    path('all_dc_skus', views.all_dc_skus, name='all_dc_skus'),
    path('edit_dc_parts/<int:pk>/', views.edit_dc_parts, name='edit_dc_parts'),
    path('all_skus', views.all_skus, name='all_skus'),
    path('all_vendors', views.all_vendors, name='all_vendors'),
    path('new_vendor', views.new_vendor, name='new_vendor'),
    path('edit_vendors/<int:pk>/', views.edit_vendors, name='edit_vendors'),
    path('new_slat', views.new_slat, name='new_slat'),
    path('all_slat_info', views.all_slat_info, name='all_slat_info'),
    path('one_stop_shop', views.one_stop_shop, name='one_stop_shop'),
    path('generate_label/<int:pk>/', views.generate_label, name='generate_label'),
    path('new_inventory_transfer', views.new_inventory_transfer, name='new_inventory_transfer'),
    path('receive_inventory_transfer/', views.receive_inventory_transfer, name='receive_inventory_transfer'),
    path('process_transfer', views.process_transfer, name='process_transfer'),
    path('quick_scan', views.process_quick_scan, name='process_quick_scan'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)