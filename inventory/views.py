from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer
from .forms import BookingForm, BookingUpdateForm, VehicleForm
from .filters import VehicleFilter
from django_filters.rest_framework import DjangoFilterBackend


def home(request):
    return render(request, 'inventory/home.html')


def vehicle_list(request):
    qs = Vehicle.objects.all()
    brand = request.GET.get('brand', '').strip()
    if brand:
        qs = qs.filter(brand__icontains=brand)
    fuel_type = request.GET.get('fuel_type', '').strip()
    if fuel_type:
        qs = qs.filter(fuel_type=fuel_type)
    available = request.GET.get('available', '')
    if available == '1':
        qs = qs.filter(is_available=True)
    elif available == '0':
        qs = qs.filter(is_available=False)
    brands = Vehicle.objects.values_list('brand', flat=True).order_by('brand').distinct()
    return render(request, 'inventory/vehicle_list.html', {'vehicles': qs, 'brands': brands})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'inventory/vehicle_detail.html', {'vehicle': vehicle})


def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle created successfully.')
            return redirect('inventory:vehicle_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm()
    return render(request, 'inventory/vehicle_form.html', {'form': form, 'is_edit': False})


def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully.')
            return redirect('inventory:vehicle_detail', pk=pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'inventory/vehicle_form.html', {'form': form, 'vehicle': vehicle, 'is_edit': True})


def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted.')
        return redirect('inventory:vehicle_list')
    return render(request, 'inventory/vehicle_confirm_delete.html', {'vehicle': vehicle})


def booking_create(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vehicle_id = pk  # always use vehicle from URL
            obj.total_days = (obj.end_date - obj.start_date).days
            obj.total_price = obj.total_days * vehicle.price_per_day
            obj.save()
            vehicle.is_available = False
            vehicle.save()
            messages.success(request, 'Booking created successfully.')
            return redirect('inventory:booking_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm(initial={'vehicle': vehicle})
    return render(request, 'inventory/booking_form.html', {'form': form, 'vehicle': vehicle})


def booking_list(request):
    bookings = Booking.objects.select_related('vehicle').order_by('-start_date')
    return render(request, 'inventory/booking_list.html', {'bookings': bookings})


def booking_update(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('vehicle'), pk=pk)
    if request.method == 'POST':
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.total_days = (obj.end_date - obj.start_date).days
            obj.total_price = obj.total_days * obj.vehicle.price_per_day
            obj.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('inventory:booking_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingUpdateForm(instance=booking)
    return render(request, 'inventory/booking_update.html', {'form': form, 'booking': booking})


def booking_delete(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('vehicle'), pk=pk)
    if request.method == 'POST':
        vehicle = booking.vehicle
        booking.delete()
        # If no other active booking for this vehicle, mark available
        if not Booking.objects.filter(vehicle=vehicle).exists():
            vehicle.is_available = True
            vehicle.save()
        messages.success(request, 'Booking deleted.')
        return redirect('inventory:booking_list')
    return render(request, 'inventory/booking_confirm_delete.html', {'booking': booking})


class VehicleSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VehicleFilter


class BookingSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

