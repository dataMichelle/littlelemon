from django.contrib import admin
from .models import Menu, Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'reservation_date', 'reservation_slot', 'formatted_time')
    list_filter = ('reservation_date', 'reservation_slot')
    search_fields = ('first_name', 'reservation_date')
    ordering = ('-reservation_date', 'reservation_slot')
    
    def formatted_time(self, obj):
        """Display reservation slot as formatted time"""
        hour = obj.reservation_slot
        ampm = 'AM' if hour < 12 else 'PM'
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
        return f'{hour} {ampm}'
    formatted_time.short_description = 'Time'

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'menu_item_description')
    search_fields = ('name', 'menu_item_description')
    ordering = ('name',)