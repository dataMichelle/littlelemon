from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views

# Create router for BookingViewSet
router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),  # Include restaurant URLs at root level
    path('restaurant/booking/', include(router.urls)),
]
