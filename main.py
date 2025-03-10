from flask import Flask, render_template, send_file, Response, jsonify
import requests
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get API key from .env file
weather_api_key = os.getenv('WEATHER_API_KEY')

# Define API endpoints
def get_weather(city, weather_api_key):
      try:
          api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"   
          get_info = requests.get(api_url)
          response = get_info.json()
          name = response['name']
          data = response['weather'][0]['description']
          temp = response['main']['temp'] - 273.15
          humidity = response['main']['humidity']
          country = response['sys']['country']
          wind_speed = response['wind']['speed']
          visibility = response['visibility']
          return render_template('weather.html', 
                                 data=data, 
                                 temp=temp, 
                                 humidity=humidity, 
                                 name=name, 
                                 country=country, 
                                 wind_speed=wind_speed, 
                                 visibility=visibility)
      except:
          error = 'City not found'
          return render_template('error.html', error=error)
# Define routes
@app.route('/weather/<city>')
def weather(city):
    return get_weather(city, weather_api_key)

@app.route('/')
def data():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)