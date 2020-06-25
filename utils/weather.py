import emojis
import pyowm

owm = pyowm.OWM('2f0c626661e9ac05ed2f4fc7c9117997')

def get_forecast(place):
    observation = owm.weather_at_place(place)
    weather = observation.get_weather()
    temperature = weather.get_temperature('celsius')["temp"]
    wind = weather.get_wind()['speed']
    clouds = weather.get_clouds()
    humidity = weather.get_humidity()
    forecast = emojis.encode(f":house: In {place} is currently {weather.get_detailed_status()} \n️:thermometer: {temperature} °C \n:dash: {wind} m/s \n:cloud: {clouds} % \n:sweat_drops: {humidity} %")
    return forecast