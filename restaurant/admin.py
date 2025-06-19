from django.contrib import admin
from .models import Menu, Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'booking_date', 'no_of_guests')
    list_filter = ('booking_date',)
    search_fields = ('name', 'booking_date')
    ordering = ('-booking_date',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'menu_item_description')
    search_fields = ('name', 'menu_item_description')
    ordering = ('name',)