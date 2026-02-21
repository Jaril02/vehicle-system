from rest_framework import serializers
from .models import Vehicle, Booking
from datetime import date


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_price','total_days']
    
    def validate(self, data):
        vehicle=data['vehicle']
        start_date=data['start_date']
        end_date=data['end_date']
        phone=data['customer_phone']
        
        if start_date <date.today():
            raise serializers.ValidationError("Start date must be today or in the future.")
        elif end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")
        if not phone.isdigit() or len(phone) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        
        overlapping_bookings = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("The vehicle is not available for the selected dates.")
        return data 
    
    def create(self, validated_data):
        vehicle=validated_data['vehicle']
        start_date=validated_data['start_date']
        end_date=validated_data['end_date']
        
        days=(end_date-start_date).days
        validated_data['total_days'] = days
        total_price=days*vehicle.price_per_day
        validated_data['total_price']=total_price


        vehicle.is_available=False
        vehicle.save()
        return super().create(validated_data)
    