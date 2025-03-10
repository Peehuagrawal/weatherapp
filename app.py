from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_weather_and_forecast(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current_weather = {
            "city": data["city"]["name"],
            "temperature": round(data["list"][0]["main"]["temp"]),
            "description": data["list"][0]["weather"][0]["description"],
            "icon": data["list"][0]["weather"][0]["icon"],
            "humidity": data["list"][0]["main"]["humidity"],
            "visibility": data["list"][0]["visibility"] // 1000,  # Convert to km
            "pressure": data["list"][0]["main"]["pressure"],
            "feels_like": round(data["list"][0]["main"]["feels_like"])
        }
        
        forecast = []
        for item in data["list"][1:6]:  # Next 5 time steps
            forecast.append({
                "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                "temperature": round(item["main"]["temp"]),
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            })
        
        return current_weather, forecast
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    if request.method == 'POST':
        city = request.form['city']
        api_key = "753d10d144772283bfde958335f7e091"  # Replace with your actual API key
        weather_data, forecast_data = get_weather_and_forecast(city, api_key)
    return render_template('index.html', weather=weather_data, forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)