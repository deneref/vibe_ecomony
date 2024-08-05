import requests
import csv
from datetime import datetime, timedelta

BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'
BASE_URL_FORECAST = 'https://api.open-meteo.com/v1/forecast'
LATITUDE = 55.7558  # Latitude for Moscow
LONGITUDE = 37.6173  # Longitude for Moscow
START_DATE = '2024-06-22'
END_DATE = '2024-07-26'

FORECAST_START_DATE = datetime.today().date()  # Today's date
FORECAST_END_DATE = datetime.today().date(
) + timedelta(days=7)  # 30 days from today


def fetch_weather_data(date):
    formatted_date = date.strftime('%Y-%m-%d')
    url = f"{BASE_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={formatted_date}&end_date={
        formatted_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe/Moscow"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'daily' in data and 'temperature_2m_max' in data['daily'] and 'temperature_2m_min' in data['daily'] and 'precipitation_sum' in data['daily']:
            daily_data = data['daily']
            return {
                'temperature_max': daily_data['temperature_2m_max'][0],
                'temperature_min': daily_data['temperature_2m_min'][0],
                'precipitation_sum': daily_data['precipitation_sum'][0],
            }
    else:
        print(f"Error fetching data for {
              formatted_date}: {response.status_code}")
    return None


def fetch_forecast_weather_data():
    start_date_str = FORECAST_START_DATE.strftime('%Y-%m-%d')
    end_date_str = FORECAST_END_DATE.strftime('%Y-%m-%d')
    url = f"{BASE_URL_FORECAST}?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date_str}&end_date={
        end_date_str}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe/Moscow"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if True:
            dates = data['daily']['time']
            max_temps = data['daily']['temperature_2m_max']
            min_temps = data['daily']['temperature_2m_min']
            rainfalls = data['daily']['precipitation_sum']
            forecast_data = [{
                'date': dates[i],
                'temperature_avg': (max_temps[i] + min_temps[i]) / 2,
                'rainfall': rainfalls[i]
            } for i in range(len(dates))]
            return forecast_data
    else:
        print(f"Error fetching forecast data: {response.status_code}")
    return []


def main():
    start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(END_DATE, '%Y-%m-%d')
    delta = timedelta(days=1)

    with open('weather_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'temperature', 'rainfall']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        current_date = start_date
        while current_date <= end_date:
            data = fetch_weather_data(current_date)
            print(data)
            if True:
                daily_data = data
                date_str = current_date.strftime('%Y-%m-%d')
                temperature_max = daily_data['temperature_max']
                temperature_min = daily_data['temperature_min']
                rainfall = daily_data['precipitation_sum']

                if temperature_max is None:
                    break

                temperature_avg = (
                    daily_data['temperature_max'] + daily_data['temperature_min']) / 2

                writer.writerow({
                    'date': date_str,
                    'temperature': temperature_avg,
                    'rainfall': rainfall
                })
            current_date += delta
    forecast_data = fetch_forecast_weather_data()

    with open('forecast_weather_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'temperature', 'rainfall']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for data in forecast_data:
            writer.writerow({
                'date': data['date'],
                'temperature': data['temperature_avg'],
                'rainfall': data['rainfall']
            })


if __name__ == "__main__":
    main()
