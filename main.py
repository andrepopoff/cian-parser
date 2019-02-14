import requests
import csv
import time

from api_params import *


def get_response(url, request_type='GET', params=None):
    """
    Gets response from server

    :param url: Url string
    :param request_type: Request type string ('GET' or 'POST')
    :param params: Dictionary with request payload data
    :return: Server response dictionary
    """
    proxy = next(PROXY_CYCLE)
    proxies_dict = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

    time.sleep(5)

    if request_type == 'GET':
        response = requests.get(url, json=params, proxies=proxies_dict, timeout=5)
    elif request_type == 'POST':
        response = requests.post(url, json=params, proxies=proxies_dict, timeout=5)
    else:
        raise AttributeError('Request type must be GET or POST!')

    if 'json' in response.headers['Content-Type']:
        return response.json()
    else:
        print(response.text)
        raise ValueError('Content type is not json object!')


def get_request_payload(region_id, room_type, request_type, page_number, for_day_value="!1"):
    """
    Gets request payload data

    :param region_id: <class 'int'> Region id
    :param room_type: <class 'int'> Room type
    :param request_type: <class 'str'> Request type
    :param page_number: <class 'int'> Page number
    :param for_day_value: <class 'str'> Equal to '!1' if renting for a long term, or equal to '1' if renting for a day
    :return: Dictionary with request payload data
    """
    data = {
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
            "page": {
                "type": TERM,
                "value": page_number
            }
        }
    }

    if request_type in ('flatrent', 'suburbanrent'):
        data["for_day"] = {
            "type": TERM,
            "value": for_day_value
        }

    object_type_data = {
            "type": TERMS,
            "value": [
                room_type
            ]
        }

    if 'suburban' in request_type:
        data["object_type"] = object_type_data
    elif 'flat' in request_type:
        data["room"] = object_type_data
    elif 'commercial' in request_type:
        data["office_type"] = object_type_data
    else:
        raise ValueError('Unknown request type!')

    return data


def get_phones(raw_data):
    """
    Gets phones from API phones data

    :param raw_data: List with phone data
    :return: String with phones
    """
    phone_numbers = []
    for data in raw_data:
        phone_number = '+' + data['countryCode'] + data['number']
        phone_numbers.append(phone_number)
    return ', '.join(phone_numbers)


def get_address(raw_data):
    """
    Gets the address from API address data

    :param raw_data: List with address data
    :return: String with address
    """
    address = []
    for data in raw_data:
        address.append(data['title'])
    return ', '.join(address)


def write_csv(csv_file_name, data_list):
    """
    Writes data to the csv file

    :param csv_file_name: String containing csv file name
    :param data_list: list with data to write to the file
    :return: None
    """
    with open(csv_file_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data_list)


def get_object_types(request_type):
    """
    Gets dictionary with object types

    :param request_type: String of request type
    :return: Dictionary with object types
    """
    if 'suburban' in request_type:
        return SUBURBAN_OBJECT_TYPES
    elif 'flat' in request_type:
        return ROOM_TYPES
    elif 'commercial' in request_type:
        return OFFICE_TYPES
    else:
        raise ValueError('Unknown request type!')


def get_for_day_params(request_type):
    """
    Gets 'for_day' parameters

    :param request_type: String of request type
    :return: Dictionary with 'for_day' parameter
    """
    if request_type in ('flatrent', 'suburbanrent'):
        return FOR_DAY_PARAMS
    return {'more_than_one': '!1'}


def get_title(obj_id, obj_type, offer):
    """
    Gets title from object

    :param obj_id: <class 'int'> Object id
    :param obj_type: <class 'int'> Object type
    :param offer: dictionary with object data
    :return: <class 'str'> Title for advertisement
    """
    total_area = offer['totalArea']
    if obj_id in (0, 10):
        room_area = offer['roomArea'] or offer['livingArea'] or total_area
        return '{}, {}/{} м²'.format(obj_type.capitalize(), total_area, room_area)
    return '{}, {} м²'.format(obj_type.capitalize(), total_area)


def get_object_data(obj_id, obj_type, offer):
    """
    Gets id, phones, address and title from dictionary with object data

    :param obj_id: <class 'int'> Object id
    :param obj_type: <class 'int'> Object type
    :param offer: dictionary with object data
    :return: list object with id, title, address, phones
    """
    _id = offer['cianId']
    phones = get_phones(offer['phones'])
    address = get_address(offer['geo']['address'])
    title = get_title(obj_id, obj_type, offer)
    return [_id, title, address, phones]


def parse_data(region_id, obj_id, obj_type, request_type, for_day_value):
    """
    Parses data from api response and writes to csv file

    :param region_id: <class 'int'> Id of region
    :param obj_id: <class 'int'> Object id
    :param obj_type: <class 'int'> Object type
    :param request_type: <class 'str'> Request type
    :param for_day_value: <class 'str'> Equal to '!1' if renting for a long term, or equal to '1' if renting for a day
    :return: None
    """
    page = 1
    while True:
        request_payload = get_request_payload(region_id, obj_id, request_type, page, for_day_value)
        response = get_response(SEARCH_OFFERS_URL, 'POST', request_payload)

        if response['status'] == 'ok':
            for offer in response['data']['offersSerialized']:
                data_list = get_object_data(obj_id, obj_type, offer)
                write_csv('{}-{}.csv'.format(request_type, region_id), data_list)

            if response['data']['suggestOffersSerializedList']:
                break

        page += 1


def main():
    """
    The main function that controls other functions, prepares data, parses and writes

    :return: None
    """
    all_regions_data = get_response(ALL_REGIONS_URL)
    if all_regions_data['status'] == 'ok':

        # Walk through all regions
        for region_data in all_regions_data['data']['items']:

            # Go through all types of request
            for request_type in REQUEST_TYPES:
                for_day_params = get_for_day_params(request_type)

                # Go through all "for_day" values
                for day_type, day_value in for_day_params.items():
                    object_types_dict = get_object_types(request_type)

                    # Go through all object types
                    for obj_type, obj_id in object_types_dict.items():
                        parse_data(region_data['id'], obj_id, obj_type, request_type, day_value)

if __name__ == '__main__':
    main()
