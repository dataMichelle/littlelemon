from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('menu-items/', views.MenuItemsView.as_view()),               # explicit generic views for menu
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),
    path('message/', views.msg),
    path('api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),  # ViewSets routes registered here (users, bookings),

]
