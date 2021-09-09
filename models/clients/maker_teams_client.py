from models.clients.base_client import BaseClient


class MTClient(BaseClient):

    credentials = {
        'token': '123123'
    }
    url = 'http://0.0.0.0:8081'

    @classmethod
    def create_new(cls, route, data):
        return super().create(route, data)
    
    @classmethod
    def create_new_user(cls, route, data):
        return super().create_user(route, data)

    @classmethod
    def delete(cls, route, data=None):
        return super().delete(route, data)

    @classmethod
    def get_all(cls, route, extra_data=None):
        return super().get_all(route, extra_data)
    
    @classmethod
    def get_one(cls, route, extra_data=None):
        return super().get_one(route, extra_data)
    
    @classmethod
    def get_by_attribute_and_value(cls, route, extra_data=None):
        return super().get_one(route, extra_data)
    
    @classmethod
    def update_by_id(cls, route, attribute, value, extra_data=None):
        return super().update_by_id(route, attribute, value, extra_data)