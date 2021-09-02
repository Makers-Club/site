import requests


def parameters(cls, route, extra_data):
    url = f'{cls.url}/{route}?'
    data = cls.credentials
    if extra_data:
        data.update(extra_data)
    parameters = ''
    for k, v in data.items():
        if parameters:
            parameters += '&'
        parameters += f'{str(k)}={str(v)}'
    return f'{url}{parameters}'

def prepare_data(cls, route, extra_data):
    url = f'{cls.url}/{route}?'
    data = cls.credentials
    if extra_data:
        data.update(extra_data)
    return url, data


class BaseClient():

    @classmethod
    def create_user(cls, route, extra_data=None):
        url, data = prepare_data(cls, route, extra_data)
        url += 'token=123123'
        response = requests.post(url, data=data)
        if not response:
            return None
        return response.json()
    
    @classmethod
    def create(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        response = requests.post(url)
        # print('IN BASE', response)
        if not response:
            return None
        return response.json()

    @classmethod
    def get_all(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        response = requests.get(url)
        # print(url, 'url')
        # print(response)
        if not response:
            return None
        return response.json()

    @classmethod
    def get_one(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        response = requests.get(url)
        if not response:
            return None
        return response.json()
    
    @classmethod
    def get_by_attribute_and_value(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.get(url).json()

    @classmethod
    def update_by_id(cls, route, attribute, value, extra_data=None):
        route = f'{route}/{attribute}/{value}'
        url = parameters(cls, route, extra_data)
        return requests.put(url).json()

    # each class adds attr + value to create route
    @classmethod
    def update_all_where(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.get(url).json()

    @classmethod
    def delete(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.delete(url).json()


