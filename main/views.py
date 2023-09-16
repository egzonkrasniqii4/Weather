from django.shortcuts import render
import json
import urllib.request

def index(request):
    if request.method == 'POST':
        city = request.POST['city']

        # Your OpenWeatherMap API key
        api_key = 'b03131b520e8a1c6ef7822b0eb21deaf'

        # Build the URL for the API request
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b03131b520e8a1c6ef7822b0eb21deaf'

        try:
            # Make a request to the API and read the response
            source = urllib.request.urlopen(url).read()

            # Convert JSON data to a dictionary
            weather_data = json.loads(source)

            # Check if the API response contains an error message
            if weather_data.get('cod') == '404':
                error_message = "City not found. Please enter a valid city name."
                data = {'error_message': error_message}
            else:
                # Extract weather information and convert temperature to Celsius
                temperature_kelvin = weather_data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15  # Convert Kelvin to Celsius

                # Create a dictionary with the weather data
                data = {
                    'city': city,
                    "country_code": str(weather_data['sys']['country']),
                    "coordinate": str(weather_data['coord']['lon']) + ' ' + str(weather_data['coord']['lat']),
                    "temp": f"{temperature_celsius:.2f}°C",
                    "pressure": str(weather_data['main']['pressure']),
                    "humidity": str(weather_data['main']['humidity']),
                }
        except Exception as e:
            # Handle other exceptions that may occur during the API request
            error_message = "City not found. Please enter a valid city name."
            data = {'error_message': error_message}
            print(str(e))
    else:
        data = {}

    return render(request, "index.html", data)
