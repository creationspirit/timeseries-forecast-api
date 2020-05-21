from django.db import models
from django.contrib.postgres.fields import JSONField


class Prediction(models.Model):
    data = models.FileField()
    seasonal_period = models.IntegerField(default=1)
    frequency = models.CharField(max_length=10)
    forecast_periods = models.IntegerField(default=0)
    result = JSONField(null=True)
