import requests
import csv
import time
import random

import api_params


class CianParser:
    """
    Class to parse data from https://www.cian.ru/
    """
    def __init__(self, proxies):
        """
        Initial method

        :param proxies: String with proxy file name (should be .txt format)
        """
        self.proxy_file_name = proxies

        # API parameters
        self.__all_regions_url = api_params.ALL_REGIONS_URL
        self.__request_types = api_params.REQUEST_TYPES
        self.__search_offers_url = api_params.SEARCH_OFFERS_URL
        self.__for_day_params = api_params.FOR_DAY_PARAMS
        self.__suburban_object_types = api_params.SUBURBAN_OBJECT_TYPES
        self.__room_types = api_params.ROOM_TYPES
        self.__office_types = api_params.OFFICE_TYPES
        self.__engine_version = api_params.ENGINE_VERSION

    def get_proxies(self):
        """
        Reads proxies from txt file

        :return: List with proxies
        """
        with open(self.proxy_file_name, 'r') as file:
            return file.readlines()

    def get_response(self, url, request_type='GET', params=None):
        """
        Gets response from server

        :param url: Url string
        :param request_type: Request type string ('GET' or 'POST')
        :param params: Dictionary with request payload data
        :return: Server response dictionary
        """
        time.sleep(10)

        for _ in range(20):
            proxy = random.choice(self.get_proxies())
            proxy_dict = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

            try:
                if request_type == 'GET':
                    response = requests.get(url, json=params, proxies=proxy_dict, timeout=10)
                elif request_type == 'POST':
                    response = requests.post(url, json=params, proxies=proxy_dict, timeout=10)
                else:
                    raise AttributeError('Request type must be GET or POST!')
            except requests.exceptions.ProxyError:
                pass
            else:
                if 'json' in response.headers['Content-Type']:
                    return response.json()
                else:
                    print(response.text)
                    raise ValueError('Content type is not json object!')

    @staticmethod
    def add_object_type_to_request_payload(room_type, request_type, data):
        """
        Adds object type data to the request payload data

        :param room_type: <class 'int'> Room type
        :param request_type: <class 'str'> Request type
        :param data: Dictionary with request payload data
        :return: None
        """
        object_type_data = {
            "type": api_params.TERMS,
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

    def get_request_payload(self, region_id, room_type, request_type, page_number, for_day_val="!1"):
        """
        Gets request payload data

        :param region_id: <class 'int'> Region id
        :param room_type: <class 'int'> Room type
        :param request_type: <class 'str'> Request type
        :param page_number: <class 'int'> Page number
        :param for_day_val: <class 'str'> Equal to '!1' if renting for a long term, or equal to '1' if renting for a day
        :return: Dictionary with request payload data
        """
        data = {
            "jsonQuery": {
                "region": {
                    "type": api_params.TERMS,
                    "value": [
                        region_id
                    ]
                },
                "_type": request_type,
                "engine_version": {
                    "type": api_params.TERM,
                    "value": self.__engine_version
                },
                "page": {
                    "type": api_params.TERM,
                    "value": page_number
                }
            }
        }

        if request_type in ('flatrent', 'suburbanrent'):
            data["for_day"] = {
                "type": api_params.TERM,
                "value": for_day_val
            }

        self.add_object_type_to_request_payload(room_type, request_type, data)
        return data

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def get_object_types(self, request_type):
        """
        Gets dictionary with object types

        :param request_type: String of request type
        :return: Dictionary with object types
        """
        if 'suburban' in request_type:
            return self.__suburban_object_types
        elif 'flat' in request_type:
            return self.__room_types
        elif 'commercial' in request_type:
            return self.__office_types
        else:
            raise ValueError('Unknown request type!')

    def get_for_day_params(self, request_type):
        """
        Gets 'for_day' parameters

        :param request_type: String of request type
        :return: Dictionary with 'for_day' parameter
        """
        if request_type in ('flatrent', 'suburbanrent'):
            return self.__for_day_params
        return {'more_than_one': '!1'}

    @staticmethod
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

    def get_object_data(self, obj_id, obj_type, offer):
        """
        Gets id, phones, address and title from dictionary with object data

        :param obj_id: <class 'int'> Object id
        :param obj_type: <class 'int'> Object type
        :param offer: dictionary with object data
        :return: list object with id, title, address, phones
        """
        _id = offer['cianId']
        phones = self.get_phones(offer['phones'])
        address = self.get_address(offer['geo']['address'])
        title = self.get_title(obj_id, obj_type, offer)
        return [_id, title, address, phones]

    def parse_data(self, region_id, obj_id, obj_type, request_type, for_day_val):
        """
        Parses data from api response and writes to csv file

        :param region_id: <class 'int'> Id of region
        :param obj_id: <class 'int'> Object id
        :param obj_type: <class 'int'> Object type
        :param request_type: <class 'str'> Request type
        :param for_day_val: <class 'str'> Equal to '!1' if renting for a long term, or equal to '1' if renting for a day
        :return: None
        """
        page = 1
        while True:
            request_payload = self.get_request_payload(region_id, obj_id, request_type, page, for_day_val)
            response = self.get_response(self.__search_offers_url, 'POST', request_payload)

            if response['status'] == 'ok':
                for offer in response['data']['offersSerialized']:
                    data_list = self.get_object_data(obj_id, obj_type, offer)
                    self.write_csv('{}-{}.csv'.format(request_type, region_id), data_list)

                if response['data']['suggestOffersSerializedList']:
                    break

            page += 1

    def run(self):
        """
        The main function that controls other functions, prepares data, parses and writes

        :return: None
        """
        all_regions_data = self.get_response(self.__all_regions_url)
        if all_regions_data['status'] == 'ok':

            # Walk through all regions
            for region_data in all_regions_data['data']['items']:

                # Go through all types of request
                for request_type in self.__request_types:
                    for_day_params = self.get_for_day_params(request_type)

                    # Go through all "for_day" values
                    for day_type, day_value in for_day_params.items():
                        object_types_dict = self.get_object_types(request_type)

                        # Go through all object types
                        for obj_type, obj_id in object_types_dict.items():
                            self.parse_data(region_data['id'], obj_id, obj_type, request_type, day_value)


if __name__ == '__main__':
    parser = CianParser(proxies='proxies.txt')
    parser.run()
