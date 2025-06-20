from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from LittleLemonAPI import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('LittleLemonAPI.urls')),
    path('', include('restaurant.urls')),

    path('auth/', include('djoser.urls')),  # Djoser routes for user management
    path('auth/', include('djoser.urls.authtoken')),  # Djoser token auth routes
]
