
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    fuel = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    mileage = models.IntegerField()
    owners = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")
    created_at = models.DateTimeField(auto_now_add=True)
    from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    ROLE_CHOICES = (
        ('dealer', 'Dealer'),
        ('customer', 'Customer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20)  # dealer or customer

    approved = models.BooleanField(default=False)  # dealer approval

    def __str__(self):
        return self.user.username