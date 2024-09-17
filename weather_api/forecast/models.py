from django.db import models

# Create your models here.

from django.utils import timezone

class APIRequestLog(models.Model):
    request_time = models.DateTimeField(default=timezone.now)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    forecast_date = models.DateTimeField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()

    def __str__(self):
        return f'{self.request_time} ,{self.city}, {self.country} - {self.forecast_date}'