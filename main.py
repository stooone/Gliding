#!/usr/bin/env python2

# Requirements:
#   pip2.7 install metar


from metar import Metar
import requests
from datetime import datetime, timedelta
import csv
import pprint
import re
import os
import pickle


pp = pprint.PrettyPrinter(indent=4)

proxy = {
    #'http': '...',
    #'https': '...',
}

def dt_parse(t):
    ret = datetime.strptime(t[0:18],'%Y-%m-%dT%H:%M:%S')
    if t[19] == '+':
       ret -= timedelta(hours=int(t[20:22]), minutes=int(t[23:]))
    elif t[19] == '-':
       ret += timedelta(hours=int(t[20:22]), minutes=int(t[23:]))
    return ret

def get_coordinates(icao):

    if not os.path.isfile('stations.txt'):
        r = requests.get('https://www.aviationweather.gov/docs/metar/stations.txt', proxies=proxy)
        with open('stations.txt', 'wb') as f:
            f.write(r.content)

    stations = open('stations.txt')
    for station in stations:
        m = re.search('.+' + weather_station, station)

        if m:
            lat_deg = station[38:41]
            lat_min = station[42:44]
            lat_side = station[44]
            lon_deg = station[47:50]
            lon_min = station[51:53]
            lon_side = station[53]
            lat = float(lat_deg) + float(lat_min) / 60
            if lat_side == 'S':
                lat *= -1
            lon = float(lon_deg) + float(lon_min) / 60
            if lon_side == 'W':
                lon *= -1

    stations.close()

    return (lat, lon)


def daylight(icao):

    cache = {}

    now = datetime.utcnow()

    if os.path.isfile('daylight.cache'):
        cache_file = open('daylight.cache', 'rb')
        cache = pickle.load(cache_file)
        cache_file.close()

    if icao in cache and cache[icao]['date'] + timedelta(days=7) > now:

        sunrise = cache[icao]['sunrise']
        sunset = cache[icao]['sunset']

    else:

        (lat, lon) = get_coordinates(icao)

        resp = requests.get('https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&formatted=0', proxies=proxy)
        json = resp.json()

        sunrise = dt_parse(json['results']['sunrise'])
        sunset = dt_parse(json['results']['sunset'])

        cache[icao] = { 'sunrise': sunrise, 'sunset': sunset, 'date': now }

        cache_file = open("daylight.cache", "wb")
        pickle.dump(cache, cache_file)
        cache_file.close()

    if sunrise.hour + sunrise.minute / 60 < now.hour + now.minute / 60 and now.hour + now.minute / 60 < sunset.hour + sunset.minute / 60:
        return True
    else:
        return False


airports_csv = open('airports.csv', 'rb')
airports = csv.reader(airports_csv, delimiter=';')

for airport in airports:

    if len(airport) < 4:
        continue

    icao = airport[0]
    weather_station = airport[1]
    min_cloud_base = int(airport[2])
    desired_wind_dir = int(airport[3])

    daylight_ok = daylight(icao)
    wind_dir_ok = False
    wind_speed_ok = False
    cloud_base_ok = False

    resp = requests.get('http://tgftp.nws.noaa.gov/data/observations/metar/stations/' + weather_station + '.TXT', proxies=proxy)
    metar = resp.text.splitlines()[1]
    decoded_metar = Metar.Metar(metar)

    cloud_base = 10000000
    if len(decoded_metar.sky) > 0:
        if decoded_metar.sky[0][1] is not None:
            cloud_base = int(decoded_metar.sky[0][1].value())
            if cloud_base > min_cloud_base:
                cloud_base_ok = True
    else:
        cloud_base_ok = True
 
    wind_dir = 0
    if decoded_metar.wind_dir is not None:
        wind_dir = int(decoded_metar.wind_dir.value())
        if (desired_wind_dir + 360 - 45 < wind_dir + 360 and desired_wind_dir + 360 + 45 > wind_dir + 360) or desired_wind_dir == -1:
            wind_dir_ok = True

    wind_speed = int(decoded_metar.wind_speed.value())
    if wind_speed > 10:
        wind_speed_ok = True

    if cloud_base_ok and daylight_ok:
        if wind_dir_ok:
            if wind_speed_ok:
                status = "OK   "
            else:
                status = "WEAK "
        else:
            status = "SO-SO"
    else:
        status = "BAD  "

    output_string = icao + ": " + status + " ("
    if daylight_ok:
        output_string += "day"
    else:
        output_string += "night/unknown"
    output_string += ", cloud base: " + str(cloud_base) + " / " + str(min_cloud_base) + ", wind: " + str(wind_speed) + "@" + str(wind_dir) + " / " + str(desired_wind_dir) + ", " + metar + ")"

    print output_string
