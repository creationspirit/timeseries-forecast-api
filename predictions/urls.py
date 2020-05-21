from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from predictions.views import PredictionListView, PredictionDetailView

urlpatterns = [
    path('', PredictionListView.as_view(), name='prediction_list'),
    path('<slug:uuid>', PredictionDetailView.as_view(), name='prediction_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
