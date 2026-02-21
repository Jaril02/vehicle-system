from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home,
    vehicle_list,
    vehicle_detail,
    vehicle_create,
    vehicle_update,
    vehicle_delete,
    booking_create,
    booking_list,
    booking_update,
    booking_delete,
    VehicleSet,
    BookingSet,
)

app_name = 'inventory'

router = DefaultRouter()
router.register('vehicles', VehicleSet)
router.register('bookings', BookingSet)

urlpatterns = [
    path('', home, name='home'),
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/create/', vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/', vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:pk>/update/', vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', vehicle_delete, name='vehicle_delete'),
    path('vehicles/<int:pk>/book/', booking_create, name='booking_create'),
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/<int:pk>/update/', booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', booking_delete, name='booking_delete'),
    path('api/', include(router.urls)),
]
