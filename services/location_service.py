# https://www.w3resource.com/python-exercises/geopy/python-geopy-nominatim_api-exercise-6.php
import geocoder
import socket
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def get_city(host):
    if host == "127.0.0.1:8000":
        ip_address = "me"

    else:
        ip_address = socket.gethostbyname(str(host))
        ip_address = str(ip_address)
    g = geocoder.ip(ip_address)
    latlng = g.latlng
    lat = latlng[0]
    lon = latlng[1]
    place = city_state_country(str(lat) + ', ' + str(lon))
    return place[1]


def city_state_country(coord):
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    return city, state, country