from django.urls import path
from .views import WeatherForecastAPIView

urlpatterns = [
    path('weather/', WeatherForecastAPIView.as_view(), name='weather-forecast'),
]
