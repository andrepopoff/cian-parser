""" This file contains all api parameters. """

BASE_API_URL = 'https://api.cian.ru/'

OBJECT_URLS = {
    'new_buildings': BASE_API_URL + 'newbuilding-search/v1/get-newbuildings-for-serp/',
    'villages': BASE_API_URL + 'countryside-search/v1/get-village-list/',
    'another_objects': BASE_API_URL + 'search-offers/v2/search-offers-desktop/',
}

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
    'студия': 9
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
    'house': 1,
    'land': 3,
    'townhouse': 4
}

OFFICE_TYPES = {
    'office': 1,
    'commercial_space': 2,
    'storage': 3,
    'premises': 5,
    'garage': 6
}

TERM = 'term'
TERMS = 'terms'
