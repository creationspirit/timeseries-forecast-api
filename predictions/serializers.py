from rest_framework import serializers

from predictions.models import Prediction


class SubmitForecastTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            'id', 'data', 'seasonal_period', 'frequency',
            'forecast_periods',
        ]


class ForecastResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'result', ]
