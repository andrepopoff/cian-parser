""" This file contains all api parameters. """

BASE_API_URL = 'https://api.cian.ru/'

OBJECT_URLS = {
    'new_buildings': BASE_API_URL + 'newbuilding-search/v1/get-newbuildings-for-serp/',
    'villages': BASE_API_URL + 'countryside-search/v1/get-village-list/',
    'another_objects': BASE_API_URL + 'search-offers/v2/search-offers-desktop/',
}

ALL_REGIONS_URL = 'https://www.cian.ru/cian-api/site/v1/get-regions/'

ROOM_TYPES = {
    'only_room': 0,
    'one_room': 1,
    'two_room': 2,
    'three_room': 3,
    'four_room': 4,
    'five_room': 5,
    'six_room': 6,
    'open_plan': 7,
    'studio': 9
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
