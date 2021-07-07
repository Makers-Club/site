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
    def create(cls, route, extra_data=None):
        url, data = prepare_data(cls, route, extra_data)
        return requests.post(url, data=data).json()

    @classmethod
    def get_all(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.get(url).json()

    @classmethod
    def get_one(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.get(url).json()
    
    @classmethod
    def get_by_attribute_and_value(cls, route, extra_data=None):
        url = parameters(cls, route, extra_data)
        return requests.get(url).json()

    @classmethod
    def update_by_id(cls, route, extra_data=None):
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

