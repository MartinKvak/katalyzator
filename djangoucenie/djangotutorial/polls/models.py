from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return f"{self.brand} {self.name}"


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def total_price(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            return days * self.car.price_per_day
        return 0

    def __str__(self):
        return f"{self.car.name} ({self.start_date} - {self.end_date})"
    
