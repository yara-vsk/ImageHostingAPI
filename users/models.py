from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Tier(models.Model):
    name = models.CharField(max_length=100)
    link_originally_image = models.BooleanField()
    expiring_links = models.BooleanField()
    thumbnail_sizes = models.CharField(max_length=100, help_text='Comma-separated list of thumbnail heights.')


    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE )
    REQUIRED_FIELDS =['tier']

    def __str__(self):
        return self.username