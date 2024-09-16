from django.urls import path
from .views import WeatherForecastAPIView, weather_form_view  # Asegúrate de importar tu vista correctamente

urlpatterns = [
    path('', weather_form_view, name='weather_form'),  # Ruta para mostrar el formulario
]
