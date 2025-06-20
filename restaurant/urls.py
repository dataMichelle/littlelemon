from rest_framework.routers import DefaultRouter
from LittleLemonAPI import views as api_views
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'tables', api_views.BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # All your API routes (viewsets) here
    path('api-auth/', include('rest_framework.urls')),  # Optional for browsable API login
]
