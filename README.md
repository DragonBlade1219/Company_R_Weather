# Weather API Project

Este proyecto es una API en Django que consulta el clima de diferentes ciudades utilizando la API de **OpenWeather** y **Reservamos** para obtener coordenadas geográficas. El objetivo es permitir a los usuarios ingresar el nombre de una ciudad y recibir un pronóstico meteorológico para los próximos 7 días.

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.x (.10 o mayor)
- Git
- virtualenv (para manejar el entorno virtual)
  
## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/DragonBlade1219/Company_R_Weather
   cd Company_R_Weather
   ```

2. **Crea y activa el entorno virtual**:

   Con `virtualenv`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux o Mac
   venv\Scripts\activate      # En Windows

   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:

   Crea un archivo `.env` en la raíz del proyecto y define la siguiente variable de entorno con el valor del api_key de la API de OpenWeather de su elección:

   ```bash
   OPENWEATHER_API_KEY=tu_openweather_api_key
   ```

6. **Levanta el servidor local**:

   ```bash
   cd weather_api
   python manage.py runserver
   ```

7. **Accede a la vista**:

   Abre tu navegador y ve a la dirección: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Vista de Endpoint
**Vista para fines prácticos y uso de otra api_key**:
    Se incluyó una vista de usuario para realizar pruebas en navegador de manera más simple en la raíz del dominio de despliegue, en esta se brinda el input de la ciudad y un input para usar una api_key adicional de manera opcional.

## Endpoint principal

- **Endpoint para consultar el clima**:

  ```http
  GET /api/weather/
  ```

  ### Parámetros
  - `city`: Nombre de la ciudad a consultar (obligatorio).
  - `api_key`: (Opcional) La API key de **OpenWeather**. Si no se envía, se usa la clave por defecto configurada en el archivo `.env`.

  ### Ejemplo de uso:

  ```bash
  curl "http://127.0.0.1:8000/api/weather/?city=monterrey&api_key=tu_api_key"
  ```
  - Como se menciona, el atributo "api_key=tu_api_key" puede omitirse, ya que es parte de la funcionalidad opcional de la vista de usuario.

  ### Ejemplo de respuesta:
  ```json
  {
      "results": [
          {
            "city": "Guadalajara",
            "state": "Jalisco",
            "country": "México",
            "forecast": [
                {
                    "date": "2024-09-16 12:00:00",
                    "min_temp": 16.34,
                    "max_temp": 29.26
                },
                {
                    "date": "2024-09-17 12:00:00",
                    "min_temp": 14.59,
                    "max_temp": 30.65
                },
                {
                    "date": "2024-09-18 12:00:00",
                    "min_temp": 16.28,
                    "max_temp": 30.92
                },
                {
                    "date": "2024-09-19 12:00:00",
                    "min_temp": 17.12,
                    "max_temp": 30.81
                },
                {
                    "date": "2024-09-20 12:00:00",
                    "min_temp": 16.43,
                    "max_temp": 28.42
                },
                {
                    "date": "2024-09-21 12:00:00",
                    "min_temp": 16.07,
                    "max_temp": 29.19
                },
                {
                    "date": "2024-09-22 12:00:00",
                    "min_temp": 15.71,
                    "max_temp": 28.85
                }
            ]
        }
      ]
  }
  ```

## Notas adicionales

- Asegúrate de tener una clave válida para la API de **OpenWeather**.
- El proyecto utiliza el puerto `8000` de manera predeterminada.

## Contribución

1. Haz un fork del proyecto.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza un commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
4. Realiza un push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Estructura del proyecto con Django:
```
Company_R_Weather:

├─ .gitignore
├─ README.md
├─ requirements.txt
└─ weather_api
   ├─ forecast
   │  ├─ __init__.py
   │  ├─ admin.py
   │  ├─ api_urls.py # archivo de urls para ruta del endpoint principal solicitado.
   │  ├─ apps.py
   │  ├─ migrations
   │  │  └─ __init__.py
   │  ├─ models.py
   │  ├─ templates
   │  │  └─ forecast
   │  │     └─ weather_form.html
   │  ├─ tests.py
   │  ├─ urls.py # archivo de urls para ruta del formulario de la vista de usuario.
   │  └─ views.py # Vista con la lógica de funcionamiento de interacción con API's.
   ├─ manage.py
   └─ weather_api
      ├─ __init__.py
      ├─ asgi.py
      ├─ settings.py #  Archivo de configuraciones de Django.
      ├─ urls.py
      └─ wsgi.py

```