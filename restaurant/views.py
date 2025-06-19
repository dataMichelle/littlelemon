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
            booking_date=data['booking_date'],
            name=data['name']
        ).exists()
        
        if exist:
            # If the reservation exists, return an error response
            return JsonResponse({'error': 'This booking already exists'}, status=400)

        # If no existing booking, create a new booking
        booking = Booking(
            name=data['name'],
            booking_date=data['booking_date'],
            no_of_guests=data.get('no_of_guests', 1),
        )
        booking.save()

        # Return success response
        return JsonResponse({'success': 'Reservation created successfully'}, status=201)
    
    # Handle GET requests
    date = request.GET.get('date')
    if date:
        bookings = Booking.objects.filter(booking_date=date)
    else:
        bookings = Booking.objects.all()
    
    # Check if this is an AJAX request (from book.html)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'bookings' in request.path:
        # Return JSON data for AJAX requests
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')
    else:
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
