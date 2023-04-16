from django.urls import path
from . import views

urlpatterns = [
    path("getPrediction", views.getPrediction, name="getPrediction"),
    path("getPredictions", views.getPredictions, name="getPredictions"),
    path("getStatistic", views.getStatistic, name="getStatistic"),
    path("getStatistics", views.getStatistics, name="getStatistics"),
]