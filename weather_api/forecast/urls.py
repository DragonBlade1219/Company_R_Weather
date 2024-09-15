from django.urls import path
from .views import WeatherForecastAPIView
from . import views

urlpatterns = [
    path('weather/', WeatherForecastAPIView.as_view(), name='weather-forecast'),
    path('', views.weather_form_view, name='weather_form'),  # Ruta para mostrar el formulario
    path('get-weather/', views.WeatherForecastAPIView.as_view(), name='get_weather'),  # Ruta para consultar el clima

]