#!/usr/bin/env python2

# Requirements:
#   pip2.7 install metar

# stations.txt: https://www.aviationweather.gov/docs/metar/stations.txt


from metar import Metar
import requests
from datetime import datetime, timedelta
import csv
import pprint
import re

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


airports_csv = open('airports.csv', 'rb')
airports = csv.reader(airports_csv, delimiter=';')

for airport in airports:

    icao = airport[0]
    weather_station = airport[1]
    min_cloud_base = int(airport[2])
    desired_wind_dir = int(airport[3])

    daylight = "UNKNOWN"
    stations =  open('stations.txt')
    for station in stations:
        m = re.search('.+' + weather_station, station)

        if m:
            lat_deg = station[38:41]
            lat_min = station[42:44]
            lat_side = station[44]
            lon_deg = station[47:50]
            lon_min = station[51:53]
            lon_side = station[53]
            lat = float(lat_deg) + float(lat_min)/60
            if lat_side == 'S':
                lat *= -1
            lon = float(lon_deg) + float(lon_min) / 60
            if lon_side == 'W':
                lon *= -1

            resp = requests.get('https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&formatted=0', proxies=proxy)
            json = resp.json()
            sunrise = dt_parse(json['results']['sunrise'])
            sunset = dt_parse(json['results']['sunset'])

            now = datetime.utcnow()

            if sunrise < now and now < sunset:
                daylight = "DAY"
            else:
                daylight = "NIGHT"

    stations.close()

    resp = requests.get('http://tgftp.nws.noaa.gov/data/observations/metar/stations/' + weather_station + '.TXT', proxies=proxy)
    metar = resp.text.splitlines()[1]
    decoded_metar = Metar.Metar(metar)

    cloud_base = 10000000
    if len(decoded_metar.sky) > 0:
        if decoded_metar.sky[0][1] is not None:
            cloud_base = int(decoded_metar.sky[0][1].value())

    wind_dir = 0
    if decoded_metar.wind_dir is not None:
        wind_dir = int(decoded_metar.wind_dir.value())

    wind_speed = int(decoded_metar.wind_speed.value())

    if cloud_base >  min_cloud_base and (daylight == "DAY" or daylight == "UNKNOWN"):
        if desired_wind_dir + 360 - 45 < wind_dir + 360 and desired_wind_dir + 360 + 45 > wind_dir + 360:
            if wind_speed > 10:
                state = "OK   "
            else:
                state = "WEAK "
        else:
            state = "SO-SO"
    else:
        state = "BAD  "

    print icao + ": " + state + " (" + daylight + ", cloud base: " + str(cloud_base) + " / " + str(min_cloud_base) + ", wind: " + str(wind_speed) + "@" + str(wind_dir) + " / " + str(desired_wind_dir) + ", " + metar + ")"
