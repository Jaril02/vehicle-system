from django.db import models

class Vehicle(models.Model):
    Fuel_Choice=[
        ('Petrol','Petrol'),
        ('Diesel','Diesel'),
        ('Electric','Electric'),
        ('Hybrid','Hybrid'),
    ]
    name=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    year=models.IntegerField()
    price_per_day=models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type=models.CharField(max_length=50,choices=Fuel_Choice,default='Petrol')
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"


class Booking(models.Model):
    vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=60)
    customer_phone=models.CharField(max_length=10)
    start_date=models.DateField()
    end_date=models.DateField()
    total_days=models.IntegerField(blank=True,null=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.vehicle.name}"
