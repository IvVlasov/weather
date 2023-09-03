from settings import GEO_TOKEN
import requests
# print(WEATHER_TOKEN)


def get_city_by_coordinates(lon, lat):
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey=%s&results=1&geocode=%s, %s&format=json'
    url = url % (GEO_TOKEN, lon, lat)
    headers = {'Referer': 'yandex.ru'}
    r = requests.get(url, headers=headers)
    data = r.json()

    featureMembers = data['response']['GeoObjectCollection']['featureMember']
    if featureMembers == []:
        print('no data')
        return None, None

    adr_components = featureMembers[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']
    for comp in adr_components:
        if comp['kind'] == 'locality':
            return comp['name']


def get_coorditates_by_city(city):
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey='+GEO_TOKEN+'&results=1&geocode='+city+'&format=json'
    headers = {'Referer': 'yandex.ru'}
    r = requests.get(url, headers=headers)
    data = r.json()
    print(data)

    featureMembers = data['response']['GeoObjectCollection']['featureMember']
    if featureMembers == []:
        print('no data')
        return None, None

    points = featureMembers[0]['GeoObject']['Point']['pos']
    longitude, latitude = points.split()
    return longitude, latitude


# lon, lat = get_coorditates_by_city('Ярославль')
# if not lon and not lat:
#     print('Ошибка')

# lon = 39.83023
# lat = 57.583337
# get_weather(lat, lon)

# print(get_city_by_coordinates(lon, lat))
