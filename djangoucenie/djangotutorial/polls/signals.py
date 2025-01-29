from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Rental

@receiver(post_delete, sender=Rental)
def update_car_availability_on_rental_delete(sender, instance, **kwargs):
    car = instance.car
    car.available = True
    car.save()