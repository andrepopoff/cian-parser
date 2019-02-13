import requests
import sys

from api_params import *


def get_response(url, request_type='GET', params=None):
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
    return ' '.join(phone_numbers)


def main():
    all_regions_data = get_response(ALL_REGIONS_URL)
    if all_regions_data['status'] == 'ok':
        for region_data in all_regions_data['data']['items']:
            region_id = region_data['id']

            for request_type in REQUEST_TYPES:
                for name, url in OBJECT_URLS.items():
                    if name == 'another_objects':
                        for room_type, room_id in ROOM_TYPES.items():
                            request_payload = get_request_payload(region_id, room_id, request_type, 1)
                            response = get_response(url, 'POST', request_payload)
                            if response['status'] == 'ok':
                                offers_serialized = response['data']['offersSerialized'][0]
                                cian_id = offers_serialized['cianId']
                                total_area = offers_serialized['totalArea']
                                room_area = offers_serialized['roomArea']
                                phones = get_phones(offers_serialized['phones'])
                                print(phones)
                                sys.exit(0)


if __name__ == '__main__':
    main()
