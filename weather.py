from enum import Enum
from typing import NamedTuple
import requests
import json

import tg_token as tok


Celsius = float
City = str
Wind_mps = float


class WeatherType(Enum):
    #  class for types of weather
    SUNNY = 'Ясно'
    PARTLY_CLOUDY = 'Переменная облачность'
    CLOUDY = 'Облачно'
    OVERCAST = 'Пасмурно'
    MIST = 'Дым'
    PATCHY_RAIN_POSSIBLE = 'Возможен дождь'
    PATCHY_SNOW_POSSIBLE = 'Возможен снег'
    PATCHY_SLEET_POSSIBLE = 'Возможен снег с дождем'
    PATCHY_FREEZING_DRIZZLE_POSSIBLE = 'Возможен ледяной дождь'
    THUNDERY_OUTBREAKS_POSSIBLE = 'Возможна гроза'
    BLOWING_SNOW = 'Снегопад'
    BLIZZARD = 'Метель'
    FOG = 'Туман'
    FREEZING_FOG = 'Ледяной туман'
    PATCHY_LIGHT_DRIZZLE = 'Местами мелкий дождь'
    LIGHT_DRIZZLE = 'Мелкий дождь'
    FREEZING_DRIZZLE = 'Моросит ледяной дождь'
    HEAVY_FREEZING_DRIZZLE = 'Моросит сильный ледяной дождь'
    PATCHY_LIGHT_RAIN = 'Местами мелкий дождь'
    LIGHT_RAIN = 'Мелкий дождь'
    MODERATE_RAIN_AT_TIMES = 'Временами дождь'
    MODERATE_RAIN = 'Дождь'
    HEAVY_RAIN_AT_TIMES = 'Временами сильный дождь'
    HEAVY_RAIN = 'Сильный дождь'
    LIGHT_FREEZING_RAIN = 'Легкий ледяной дождь'
    MODERATE_OR_HEAVY_FREEZING_RAIN = 'Умеренный ледяной дождь'
    LIGHT_SLEET = 'Легкий мокрый снег'
    MODERATE_OR_HEAVY_SLEET = 'Умеренный мокрый снег'
    PATCHY_LIGHT_SNOW = 'Местами мелкий снег'
    LIGHT_SNOW = 'Мелкий снег'
    PATCHY_MODERATE_SNOW = 'Местами умеренный снег'
    MODERATE_SNOW = 'Умеренный снег'
    PATCHY_HEAVY_SNOW = 'Местами сильный снег'
    HEAVY_SNOW = 'Сильный снег'
    ICE_PELLETS = 'Ледяной дождь'
    LIGHT_RAIN_SHOWER = 'Небольшой ледяной дождь'
    MODERATE_OR_HEAVY_RAIN_SHOWER = 'Умеренный или сильный ливень'
    TORRENTIAL_RAIN_SHOWER = 'Сильные ливни'
    LIGHT_SLEET_SHOWERS = 'Небольшой ливневый дождь со снегом'
    MODERATE_OR_HEAVY_SLEET_SHOWERS = (
                            'Умеренные или сильные '
                            'ливневые дожди со снегом'
                            )
    LIGHT_SNOW_SHOWERS = 'Небольшой снег'
    MODERATE_OR_HEAVY_SNOW_SHOWERS = 'Умеренный или сильный снег'
    LIGHT_SHOWERS_OF_ICE_PELLETS = 'Небольшой ледяной дождь'
    MODERATE_OR_HEAVY_SHOWERS_OF_ICE_PELLETS = (
                            'Умеренный или сильный '
                            'ледяной дождь'
                            )
    PATCHY_LIGHT_RAIN_WITH_THUNDER = (
                            'В отдельных районах местами '
                            'небольшой дождь с грозой'
                            )
    MODERATE_OR_HEAVY_RAIN_WITH_THUNDER = (
                            'В отдельных районах умеренный '
                            'или сильный дождь с грозой'
                            )
    PATCHY_LIGHT_SNOW_WITH_THUNDER = (
                            'В отдельных районах '
                            'местами небольшой снег с грозой'
                            )
    MODERATE_OR_HEAVY_SNOW_WITH_THUNDER = (
                            'В отдельных районах умеренный '
                            'или сильный снег с грозой'
                            )


class WindDirection(Enum):
    N = 'Северный'
    NNE = 'Северо-восточный'
    NE = 'Северо-восточный'
    ENE = 'Северо-восточный'
    E = 'Восточный'
    ESE = 'Юго-восточный'
    SE = 'Юго-восточный'
    SSE = 'Юго-восточный'
    S = 'Южный'
    SSW = 'Юго-западный'
    SW = 'Юго-западный'
    WSW = 'Юго-западный'
    W = 'Западный'
    NWN = 'Северо-западный'
    NW = 'Северо-западный'
    NNW = 'Северо-западный'


class Weather(NamedTuple):
    city: City
    temp: Celsius
    feels_temp: Celsius
    weather_type: WeatherType
    icon: str
    wind_dir: WindDirection
    wind_mps: Wind_mps


def get_weather_current(latitude: float, longitude: float) -> json:
    '''return a json file with current weather'''
    try:
        weather = requests.get(
            'http://api.weatherapi.com/v1/current.json?'
            f'key={tok.WEATHER}&q={latitude}, {longitude}'
            ).json()
        return weather
        #  return json.dumps(weather, indent=4, sort_keys=True)
    except UnicodeDecodeError:
        print("Can't get response from WeatherAPI")


def get_weather_forecast(latitude: float, longitude: float) -> json:
    '''return a json file with forecast weather'''
    try:
        weather = requests.get(
            'http://api.weatherapi.com/v1/forecast.json?'
            f'key={tok.WEATHER}&q={latitude}, {longitude}'
            ).json()
        return weather
        #  return json.dumps(weather, indent=4, sort_keys=True)
    except UnicodeDecodeError:
        print("Can't get response from WeatherAPI")


def _parse_weather_type(weather: json) -> WeatherType:
    weather_types = {
        1000: WeatherType.SUNNY,
        1003: WeatherType.PARTLY_CLOUDY,
        1006: WeatherType.CLOUDY,
        1009: WeatherType.OVERCAST,
        1030: WeatherType.MIST,
        1063: WeatherType.PATCHY_RAIN_POSSIBLE,
        1066: WeatherType.PATCHY_SNOW_POSSIBLE,
        1069: WeatherType.PATCHY_SLEET_POSSIBLE,
        1072: WeatherType.PATCHY_FREEZING_DRIZZLE_POSSIBLE,
        1087: WeatherType.THUNDERY_OUTBREAKS_POSSIBLE,
        1114: WeatherType.BLOWING_SNOW,
        1117: WeatherType.BLIZZARD,
        1135: WeatherType.FOG,
        1147: WeatherType.FREEZING_FOG,
        1150: WeatherType.PATCHY_LIGHT_DRIZZLE,
        1153: WeatherType.LIGHT_DRIZZLE,
        1168: WeatherType.FREEZING_DRIZZLE,
        1171: WeatherType.HEAVY_FREEZING_DRIZZLE,
        1180: WeatherType.PATCHY_LIGHT_RAIN,
        1183: WeatherType.LIGHT_RAIN,
        1186: WeatherType.MODERATE_RAIN_AT_TIMES,
        1189: WeatherType.MODERATE_RAIN,
        1192: WeatherType.HEAVY_RAIN_AT_TIMES,
        1195: WeatherType.HEAVY_RAIN,
        1198: WeatherType.LIGHT_FREEZING_RAIN,
        1201: WeatherType.MODERATE_OR_HEAVY_FREEZING_RAIN,
        1204: WeatherType.LIGHT_SLEET,
        1207: WeatherType.MODERATE_OR_HEAVY_SLEET,
        1210: WeatherType.PATCHY_LIGHT_SNOW,
        1213: WeatherType.LIGHT_SNOW,
        1216: WeatherType.PATCHY_MODERATE_SNOW,
        1219: WeatherType.MODERATE_SNOW,
        1222: WeatherType.PATCHY_HEAVY_SNOW,
        1225: WeatherType.HEAVY_SNOW,
        1237: WeatherType.ICE_PELLETS,
        1240: WeatherType.LIGHT_RAIN_SHOWER,
        1243: WeatherType.MODERATE_OR_HEAVY_RAIN_SHOWER,
        1246: WeatherType.TORRENTIAL_RAIN_SHOWER,
        1249: WeatherType.LIGHT_SLEET_SHOWERS,
        1252: WeatherType.MODERATE_OR_HEAVY_SLEET_SHOWERS,
        1255: WeatherType.LIGHT_SNOW_SHOWERS,
        1258: WeatherType.MODERATE_OR_HEAVY_SNOW_SHOWERS,
        1261: WeatherType.LIGHT_SHOWERS_OF_ICE_PELLETS,
        1264: WeatherType.MODERATE_OR_HEAVY_SHOWERS_OF_ICE_PELLETS,
        1273: WeatherType.PATCHY_LIGHT_RAIN_WITH_THUNDER,
        1276: WeatherType.MODERATE_OR_HEAVY_RAIN_WITH_THUNDER,
        1279: WeatherType.PATCHY_LIGHT_SNOW_WITH_THUNDER,
        1282: WeatherType.MODERATE_OR_HEAVY_SNOW_WITH_THUNDER
        }
    code = weather['current']['condition']['code']
    return weather_types[code]


def _parse_wind_dir(weather: json) -> WindDirection:
    wind_direction = {
        'N': WindDirection.N,
        'NNE': WindDirection.NNE,
        'NE': WindDirection.NE,
        'ENE': WindDirection.ENE,
        'E': WindDirection.E,
        'ESE': WindDirection.ESE,
        'SE': WindDirection.SE,
        'SSE': WindDirection.SSE,
        'S': WindDirection.S,
        'SSW': WindDirection.SSW,
        'SW': WindDirection.SW,
        'WSW': WindDirection.WSW,
        'W': WindDirection.W,
        'NWN': WindDirection.NWN,
        'NW': WindDirection.NW,
        'NNW': WindDirection.NNW
    }
    dir = weather['current']['wind_dir']
    return wind_direction[dir]


def _parse_weather(weather: json) -> Weather:
    return Weather(
        city=City(weather['location']['name']),
        temp=Celsius(weather['current']['temp_c']),
        feels_temp=Celsius(weather['current']['feelslike_c']),
        weather_type=_parse_weather_type(weather).value,
        icon=f'http:{weather['current']['condition']['icon']}',
        wind_dir=_parse_wind_dir(weather).value,
        wind_mps=int(Wind_mps(weather['current']['wind_kph'] / 3.6))
        )
