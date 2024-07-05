import requests
# OpenWeatherMap API endpoint
url = 'https://api.openweathermap.org/data/2.5/weather'
# Parameters for the API request
params = {
'q': 'Dhaka', # City name
'units': 'metric',
'appid': '37d0af6ce46a25155ce558cb4cc6c57d' # You get the key by subscribing (free)
}
# Send GET request to the API
response = requests.get(url, params=params)
# Check if the request was successful (status code 200)
if response.status_code == 200:
# Extract and print the weather data
    weather_data = response.json()
    print("Weather in Dhaka:")
    print("Temperature:", weather_data['main']['temp'], "C")
    print("Description:", weather_data['weather'][0]['description'])
else:
    print("Failed to retrieve weather data. Status code:", response.status_code)