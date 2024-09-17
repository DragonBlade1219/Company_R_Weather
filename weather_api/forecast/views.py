from django.shortcuts import render

# Create your views here.

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.utils import timezone as tz
from .models import APIRequestLog
from django.db import connection

class WeatherForecastAPIView(APIView, ):
    
    def get(self, request):
        # Se obtiene nombre de la petición GET.
        city_name = request.GET.get('city') 
        
        # openweather_api_key = 'a5a47c18197737e8eeca634cd6acb581' # API_KEY Proporcionada por 'R'.
        # Se obtiene el api_key de la petición, sino toma el valor por defecto del settings.
        openweather_api_key = request.GET.get('api_key', None) or settings.OPENWEATHER_API_KEY 
        if not city_name:
            return Response({'error': 'City name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener coordenadas de la ciudad desde company_r API
        company_r_url = f'https://search.reservamos.mx/api/v2/places?q={city_name}'
        company_r_response = requests.get(company_r_url)
        
        if company_r_response.status_code != 201:
            return Response({'error': 'Error fetching city data from company_r API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        cities = company_r_response.json()
        if not cities:
            return Response({'error': 'No cities found with the given name'}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener clima desde OpenWeather para cada ciudad
        forecast_results = []
        for city in cities:
            #  Solo proceder con el envío al API de OpenWeather si el campo 'result_type' es igual a'city'.
            if city.get('result_type') != 'city':
                continue
            else:
                lat = city.get('lat')
                lon = city.get('long')
                if lat and lon:
                    openweather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely,current&units=metric&appid={openweather_api_key}'
                    openweather_response = requests.get(openweather_url)
                    # print(f"Respuesta OpenAPI: ", openweather_response.json())
                    if openweather_response.status_code == 200:
                        forecast = openweather_response.json()
                        daily_forecast = forecast.get('daily', [])
                        
                        # Crear un diccionario con el pronóstico de la ciudad
                        city_forecast = {
                            'city': city.get('city_name'), 
                            'state': city.get('state'),
                            'country': city.get('country'),
                            'forecast': [
                                {
                                    'date': (datetime.fromtimestamp(day['dt'], tz=timezone.utc) + timedelta(seconds=forecast['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
                                    'min_temp': day['temp']['min'],
                                    'max_temp': day['temp']['max']
                                } for day in daily_forecast[1:8]  # Clima para los próximos 7 días
                            ]
                        }
                        
                        # Agregar los resultados a la lista
                        forecast_results.append(city_forecast)
                    elif str(openweather_response.status_code)[0] == "4":
                        # Manejo de error si la llamada a OpenWeather falla
                        print("Error!")
                        print(f"Status Code: {str(openweather_response.status_code)}" + " " + openweather_response.json().get('message'))
                        return Response({'error': openweather_response.json().get("message")}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({'error': f'Error fetching weather data from OpenWeather API.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Si no se encontraron resultados, devolver un error
        if not forecast_results:
            return Response({'error': 'No valid cities found for weather forecast'}, status=status.HTTP_404_NOT_FOUND)

        process_api_response(openweather_api_key, forecast_results)
        show_raw_api_requests(request)
        
        return Response({'results': forecast_results}, status=status.HTTP_200_OK)

# Función para poder renderizar el html:
def weather_form_view(request):
    return render(request, 'forecast/weather_form.html')

# Función de persistencia en BD:
def process_api_response(api_key, forecast_results):
    
    city_data = forecast_results[0]

    # Manejar el caso en que no haya resultados válidos
    #print("La estructura de los datos no es la esperada: ")
    #print(forecast_results.json())
    #city_data = None  # O maneja el error de otra manera adecuada para tu lógica

    # Extrae la información necesaria
    city = city_data.get('city')
    state = city_data.get('state', '')  # Opcional
    country = city_data.get('country')

    forecast_date = city_data['forecast'][0].get('date')
    min_temp = city_data['forecast'][0].get('min_temp')
    max_temp = city_data['forecast'][0].get('max_temp')

    # Guarda la información en la base de datos
    log = APIRequestLog(
        request_time=tz.now(),
        api_key=api_key,
        city=city,
        state=state,
        country=country,
        forecast_date=forecast_date,
        min_temp=min_temp,
        max_temp=max_temp
    )
    log.save()

def execute_raw_query_1():
    cities = ["Guadalajara", "Monterrey", "Cancun"]
    placeholders = ', '.join(['%s'] * len(cities))
    query = f"""
             SELECT * 
             FROM forecast_apirequestlog 
             WHERE city IN ({placeholders});
             """
    with connection.cursor() as cursor:
        cursor.execute(query, cities)
        rows = cursor.fetchall()
    return rows

def execute_raw_query_2():
    cities = ["Guadalajara", "Monterrey", "Cancun"]
    logs = APIRequestLog.objects.filter(city__in=cities)
    return logs
    # return APIRequestLog.objects.all()

def show_raw_api_requests(request):
    logs_1 = execute_raw_query_1()
    logs_2 = execute_raw_query_2()
    print(f"Logs por Native SQL: {logs_1}")
    print(f"Logs por ORM: {logs_2}")
    # return render(request, 'raw_api_requests.html', {'logs': logs})
    
# def execute_raw_query_3():
#     cities = ["Guadalajara", "Monterrey", "Cancun"]
#     placeholders = ', '.join(['%s'] * len(cities))
#     query = f"""
#              SELECT * 
#              FROM forecast_apirequestlog 
#              WHERE city IN ({placeholders});
#              """
#     logs = APIRequestLog.objects.raw(query, cities)
#     return logs