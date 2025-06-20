from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm
from .models import Menu, Booking
import json

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'book.html', {'form': form})

@csrf_exempt
def reservations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if Booking.objects.filter(booking_date=data['booking_date'], name=data['name']).exists():
            return JsonResponse({'error': 'This booking already exists'}, status=400)

        booking = Booking(
            name=data['name'],
            booking_date=data['booking_date'],
            no_of_guests=data.get('no_of_guests', 1),
        )
        booking.save()
        return JsonResponse({'success': 'Reservation created successfully'}, status=201)

    date = request.GET.get('date')
    bookings = Booking.objects.filter(booking_date=date) if date else Booking.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'bookings' in request.path:
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')

    return render(request, 'bookings.html', {'bookings': bookings})

def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {"menu": menu_data})

def display_menu_item(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk) if pk else None
    return render(request, 'menu_item.html', {"menu_item": menu_item})
