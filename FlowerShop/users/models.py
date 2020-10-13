from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django import forms
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='no_image.png', upload_to='profile_pics')

    # TODO: change mobile number regex for home number
    mobile_regex = RegexValidator(
        regex=r'(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}')
    # mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Address(models.Model):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    address_detail = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}')
    phone_number = models.CharField(max_length=15)
