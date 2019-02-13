import requests
import sys
import csv
import time

from api_params import *


def get_response(url, request_type='GET', params=None):
    time.sleep(5)
    if request_type == 'GET':
        response = requests.get(url, json=params)
    elif request_type == 'POST':
        response = requests.post(url, json=params)
    else:
        raise AttributeError('Request type must be GET or POST!')

    if 'json' in response.headers['Content-Type']:
        return response.json()
    raise ValueError('Content type is not json object!')


def get_request_payload(region_id, room_type, request_type, page_number):
    return {
        "jsonQuery": {
            "region": {
                "type": TERMS,
                "value": [
                    region_id
                ]
            },
            "_type": request_type,
            "engine_version": {
                "type": TERM,
                "value": ENGINE_VERSION_NUM
            },
            "room": {
                "type": TERMS,
                "value": [
                    room_type
                ]
            },
            "page": {
                "type": TERM,
                "value": page_number
            }
        }
    }


def get_phones(raw_data):
    phone_numbers = []
    for data in raw_data:
        phone_number = '+' + data['countryCode'] + data['number']
        phone_numbers.append(phone_number)
    return ', '.join(phone_numbers)


def get_address(raw_data):
    address = []
    for data in raw_data:
        address.append(data['title'])
    return ', '.join(address)


def write_csv(data_list):
    with open('cian.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data_list)


def main():
    all_regions_data = get_response(ALL_REGIONS_URL)
    if all_regions_data['status'] == 'ok':
        for region_data in all_regions_data['data']['items']:
            region_id = region_data['id']

            for request_type in REQUEST_TYPES:
                for name, url in OBJECT_URLS.items():
                    if name == 'another_objects':
                        for room_type, room_id in ROOM_TYPES.items():
                            page = 1
                            while True:
                                request_payload = get_request_payload(region_id, room_id, request_type, page)
                                response = get_response(url, 'POST', request_payload)

                                if response['status'] == 'ok':
                                    offers_serialized = response['data']['offersSerialized']

                                    for offer in offers_serialized:
                                        cian_id = offer['cianId']
                                        total_area = offer['totalArea']
                                        phones = get_phones(offer['phones'])
                                        address = get_address(offer['geo']['address'])

                                        if room_id == 0:
                                            room_area = offer['roomArea'] or offer['livingArea']
                                            title = '{}, {}/{} м²'.format(room_type.capitalize(), total_area, room_area)
                                        else:
                                            title = '{}, {} м²'.format(room_type.capitalize(), total_area)

                                        write_csv([cian_id, title, address, phones])

                                    if response['data']['suggestOffersSerializedList']:
                                        break

                                page += 1
                        sys.exit(0)


if __name__ == '__main__':
    main()
