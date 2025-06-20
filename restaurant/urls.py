from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets (User only now)
router = DefaultRouter()
router.register(r'api/users', views.UserViewSet)

urlpatterns = [
    # Web pages
    path('', views.index, name='index'),  # Homepage
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('bookings/', views.reservations, name='bookings'),
    path('menu/', views.menu, name='menu'),  # Menu template view
    path('menu_item/<int:pk>/', views.display_menu_item, name='menu_item'),
    
    # API endpoints as per exercise instructions
    path('menu/items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu/items/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item-detail'),

    
    # Include router URLs for ViewSets
    path('restaurant/booking/', include(router.urls)),
]
