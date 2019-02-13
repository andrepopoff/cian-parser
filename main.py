import requests
import api_params


def get_response(url, request_type='GET', params=None):
    if request_type == 'GET':
        response = requests.get(url, params=params)
    elif request_type == 'POST':
        response = requests.post(url, params=params)
    else:
        raise AttributeError('Request type must be GET or POST!')

    if 'json' in response.headers['Content-Type']:
        return response.json()


def main():
    response = get_response(api_params.OBJECT_URLS['another_objects'])

if __name__ == '__main__':
    print(main())
