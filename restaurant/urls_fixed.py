from django.urls import path
from . import views

urlpatterns = [
    # Web pages
    path('', views.index, name='index'),  # Homepage
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('bookings/', views.reservations, name='bookings'),
    path('menu/', views.menu, name='menu'),  # Menu template view
    path('menu_item/<int:pk>/', views.display_menu_item, name='menu_item'),
    
    # API endpoints
    path('api/bookings/', views.BookingList.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', views.BookingDetail.as_view(), name='booking-detail'),
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items-api'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item-detail-api'),
    path('api/users/', views.UserView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.SingleUserView.as_view(), name='user-detail'),
]
