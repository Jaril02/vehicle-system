from django import forms
from .models import Vehicle, Booking
from datetime import date


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'brand', 'year', 'price_per_day', 'fuel_type', 'is_available']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'customer_name', 'customer_phone', 'start_date', 'end_date']
        widgets = {
            'vehicle': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        data = super().clean()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')
        phone = data.get('customer_phone')

        if start_date and start_date < date.today():
            self.add_error('start_date', 'Start date must be today or in the future.')
        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', 'End date must be after start date.')
        if phone and (not phone.isdigit() or len(phone) != 10):
            self.add_error('customer_phone', 'Phone number must be 10 digits.')

        if vehicle and start_date and end_date:
            overlapping = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date,
            )
            if self.instance and self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                self.add_error(None, 'This vehicle is not available for the selected dates.')
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        vehicle = instance.vehicle
        start_date = instance.start_date
        end_date = instance.end_date
        instance.total_days = (end_date - start_date).days
        instance.total_price = instance.total_days * vehicle.price_per_day
        if commit:
            instance.save()
            vehicle.is_available = False
            vehicle.save()
        return instance


class BookingUpdateForm(forms.ModelForm):
    """Form for updating a booking (customer and dates only; vehicle fixed)."""
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_phone', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        data = super().clean()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        phone = data.get('customer_phone')

        if start_date and start_date < date.today():
            self.add_error('start_date', 'Start date must be today or in the future.')
        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', 'End date must be after start date.')
        if phone and (not phone.isdigit() or len(phone) != 10):
            self.add_error('customer_phone', 'Phone number must be 10 digits.')

        vehicle = self.instance.vehicle if self.instance else None
        if vehicle and start_date and end_date:
            overlapping = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).exclude(pk=self.instance.pk)
            if overlapping.exists():
                self.add_error(None, 'This vehicle is not available for the selected dates.')
        return data
