from django.db import models


# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=200)
    no_of_guests = models.IntegerField()
    booking_date = models.DateField()
    booking_slots = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


# Add code to create Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu_item_description = models.TextField()

    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='restaurant_users')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Restaurant User'
        verbose_name_plural = 'Restaurant Users'