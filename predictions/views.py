from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult

from predictions.serializers import (
    SubmitForecastTaskSerializer, ForecastResultSerializer
)
from predictions.predict import forecast_timeseries
from predictions.models import Prediction


class PredictionListView(APIView):
    """
    Create a forecast async job.
    """

    def post(self, request, format=None):
        serializer = SubmitForecastTaskSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.save()
            task = forecast_timeseries.delay(model.id)
            return Response(data={'task_id': task.id}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictionDetailView(APIView):
    """
    Retrieve forecast job status or result.
    """

    def get(self, request, uuid, format=None):
        result = AsyncResult(id=uuid)
        if result.ready():
            prediction_id = result.get()
            prediction = Prediction.objects.values(
                'id', 'result'
            ).get(pk=prediction_id)
            print(prediction)
            serializer = ForecastResultSerializer(prediction)
            print(serializer, serializer.data)
            return Response(serializer.data)
        return Response(data={
            'state': result.state,
            'details': result.info,
        }, status=status.HTTP_200_OK)
