""" This file contains all api parameters. """

BASE_API_URL = 'https://api.cian.ru/'
SEARCH_OFFERS_URL = BASE_API_URL + 'search-offers/v2/search-offers-desktop/'
ALL_REGIONS_URL = 'https://www.cian.ru/cian-api/site/v1/get-regions/'

ROOM_TYPES = {
    'комната': 0,
    '1-комн. квартира': 1,
    '2-комн. квартира': 2,
    '3-комн. квартира': 3,
    '4-комн. квартира': 4,
    '5-комн. квартира': 5,
    'многокомнатная квартира': 6,
    'квартира свободной планировки': 7,
    'студия': 9,
    'койко-место': 10
}

REQUEST_TYPES = (
    'flatsale',
    'flatrent',
    'suburbansale',
    'suburbanrent',
    'commercialsale',
    'commercialrent'
)

ENGINE_VERSION_NUM = 2

FOR_DAY_PARAMS = {
    'one': '1',
    'more_than_one': '!1'
}

SUBURBAN_OBJECT_TYPES = {
    'дом': 1,
    'участок': 3,
    'таунхаус': 4
}

OFFICE_TYPES = {
    'офис': 1,
    'торговая площадь': 2,
    'склад': 3,
    'помещение': 5,
    'гараж': 6
}

TERM = 'term'
TERMS = 'terms'

# PROXIES = [
#     'dIyKsL:l4uuIfl27Ri@185.154.20.95:3000/',
#     'dIyKsL:l4uuIfl27Ri@185.154.21.103:3000/',
#     'dIyKsL:l4uuIfl27Ri@185.154.21.104:3000/',
#     'dIyKsL:l4uuIfl27Ri@185.154.21.107:3000/',
#     'dIyKsL:l4uuIfl27Ri@185.154.21.108:3000/'
# ]
