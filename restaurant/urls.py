from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    
    # Update this URL pattern
    path('bookings/', views.reservations, name='bookings'),  # Render bookings HTML page

    # API endpoint to retrieve bookings in JSON format
    path('api/bookings/', views.BookingList.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', views.BookingDetail.as_view(), name='booking-detail'),
]
