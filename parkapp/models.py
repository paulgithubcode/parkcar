import math
import functools
from datetime import timedelta

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

plate_number_validator = RegexValidator("([A-Za-z]{3}\-\d{3}[A-Za-z]{2})", "Plate Number are in the format ABC-123DE")
STATUS = [('parked', 'parked'), ('exited', 'exited')]

class Park(models.Model):
    name = models.CharField(max_length=100, unique=True)
    maximum_no_cars = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=9,
                                    validators=[plate_number_validator])
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True, null=True)
    fee_paid = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS, default="parked", max_length=7)
    date_modified = models.DateTimeField(auto_now=True)
    park = models.ForeignKey(
        Park, related_name="parkingtickets", on_delete=models.CASCADE)

class Access(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    num_of_access = models.IntegerField(default=10)
    last_accessed = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
