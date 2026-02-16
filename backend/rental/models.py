from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random


class Apartment(models.Model):
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    rent = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    area = models.IntegerField(null=True, blank=True, help_text='Square feet')
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='apartments/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.apartment.title} ({self.pk})"


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expiry = models.DateTimeField()

    def mark_used(self):
        self.is_used = True
        self.save()

    @classmethod
    def create_otp_for_user(cls, user, minutes_valid=15):
        code = "%06d" % random.randint(0, 999999)
        expiry = timezone.now() + timedelta(minutes=minutes_valid)
        return cls.objects.create(user=user, code=code, expiry=expiry)

    def is_valid(self):
        return (not self.is_used) and (timezone.now() <= self.expiry)
