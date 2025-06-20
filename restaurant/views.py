from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm
from .models import Menu, Booking, User
import json
from .serializers import BookingSerializer, MenuSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions

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
    context = {'form': form}
    return render(request, 'book.html', context)

@csrf_exempt
def reservations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        exist = Booking.objects.filter(
            booking_date=data['booking_date'],
            name=data['name']
        ).exists()
        if exist:
            return JsonResponse({'error': 'This booking already exists'}, status=400)

        booking = Booking(
            name=data['name'],
            booking_date=data['booking_date'],
            no_of_guests=data.get('no_of_guests', 1),
        )
        booking.save()
        return JsonResponse({'success': 'Reservation created successfully'}, status=201)

    date = request.GET.get('date')
    if date:
        bookings = Booking.objects.filter(booking_date=date)
    else:
        bookings = Booking.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'bookings' in request.path:
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')
    else:
        context = {'bookings': bookings}
        return render(request, 'bookings.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {"menu": menu_data})

def display_menu_item(request, pk=None):
    if pk is not None:
        menu_item = get_object_or_404(Menu, pk=pk)
    else:
        menu_item = None
    return render(request, 'menu_item.html', {"menu_item": menu_item})

class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
