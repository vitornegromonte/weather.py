import argparse
from configparser import ConfigParser
import json
from urllib import parse,request

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def read_user_cli():
    parser = argparse.ArgumentParser(description= 'Gets weather and temperature for a city')

    parser.add_argument(
        'city', nargs='+', type=str, help='enter the city name'
    )
    parser.add_argument(
        '-i', 
        '--imperial',
        action = 'store_true',
        help = 'display the temperature in imperial units'
    )
    return parser.parse_args()

def build_weather_query(city_input, imperial = False):
    
    api_key = _get_api_key()
    city_name = ' '.join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f'{BASE_URL}?q={url_encoded_city_name}'
        f'&units={units}&&APIID={api_key}'
    )
    
    return url

def _get_api_key():
    config = ConfigParser()
    config.read('secrets.ini')
    return config['openweather']['api_key']

def get_weather_data(query_url):
    response = request.urlopen(query_url)
    data = response.read()
    return json.loads(data)

if __name__ == '__main__':
    user_args = read_user_cli()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    print(query_url)
    #weather_data = get_weather_data(query_url)
    