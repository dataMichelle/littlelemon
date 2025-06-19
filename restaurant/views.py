# views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm
from .models import Menu, Booking
import json
from .serializers import BookingSerializer
from rest_framework import generics


def index(request):
    return render(request, 'index.html', {})

# Helper function to format reservation slot into time format
def format_reservation_time(slot):
    """ Helper function to format reservation slot time """
    hour = slot
    ampm = 'AM' if hour < 12 else 'PM'
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
    return f'{hour} {ampm}'

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@csrf_exempt
def reservations(request):
    if request.method == 'POST':
        # Parse the incoming JSON request
        data = json.loads(request.body)
        
        # Check if the reservation already exists
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()
        
        if exist:
            # If the reservation exists, return an error response
            return JsonResponse({'error': 'This time slot is already booked'}, status=400)

        # If no existing booking, create a new booking
        booking = Booking(
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
        )
        booking.save()

        # Return success response
        return JsonResponse({'success': 'Reservation created successfully'}, status=201)
    
    # Handle GET requests
    date = request.GET.get('date')
    if date:
        bookings = Booking.objects.filter(reservation_date=date)
    else:
        bookings = Booking.objects.all()    # Check if this is an AJAX request (from book.html)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'bookings' in request.path:
        # Return JSON data for AJAX requests (keep original numeric slots)
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')
    else:
        # Format the reservation time for HTML template rendering
        for booking in bookings:
            booking.formatted_time = format_reservation_time(booking.reservation_slot)  # Adding formatted time
        
        # Pass the bookings to the 'bookings.html' template
        context = {'bookings': bookings}
        return render(request, 'bookings.html', context)

    if request.method == 'POST':
        # Parse the incoming JSON request
        data = json.loads(request.body)
        
        # Check if the reservation already exists
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()
        
        if exist:
            # If the reservation exists, return an error response
            return JsonResponse({'error': 'This time slot is already booked'}, status=400)

        # If no existing booking, create a new booking
        booking = Booking(
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
        )
        booking.save()

        # Return success response
        return JsonResponse({'success': 'Reservation created successfully'}, status=201)
    
    # Handle GET requests
    date = request.GET.get('date')
    if date:
        bookings = Booking.objects.filter(reservation_date=date)
    else:
        bookings = Booking.objects.all()    # Check if this is an AJAX request (from book.html)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'bookings' in request.path:
        # Return JSON data for AJAX requests (keep original numeric slots)
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')
    else:
        # Format the reservation time for HTML template rendering
        for booking in bookings:
            booking.formatted_time = format_reservation_time(booking.reservation_slot)
        
        # Pass the bookings to the 'bookings.html' template
        context = {'bookings': bookings}
        return render(request, 'bookings.html', context)

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item})

@csrf_exempt
def some_view_that_needs_no_csrf(request):
    # Your logic here for the view
    return HttpResponse('This view does not require CSRF protection.')
