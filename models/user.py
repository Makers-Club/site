from models.base import Base


class User(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_user(cls, client, data):
        route = 'users'
        response = client.create_new_user(route, data)
        if not response or not response.get('user'):
            return None
        user = User(**response.get('user'))
        return user
    
    def delete(self, client):
        route = f'users/{self.id}'
        response = client.delete(route)
        if not response or not response.get('status') == 'OK':
            return False
        return True

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'users'
        response = client.get_all(route, extra_data)
        if not response or not response.get('users'):
            return []
        return [User(**user_dict) for user_dict in response.get('users')]
    
    @classmethod
    def get_by_id(cls, client, id, extra_data=None) -> dict:
        route = f'users/{id}'
        response = client.get_one(route, extra_data)
        if not response or not response.get('user'):
            return None
        user = User(**response.get('user'))
        return user
    
    @classmethod
    def get_by_attribute_and_value(cls, client, attribute, value, extra_data=None):
        route = f'users/{attribute}/{value}'
        response = client.get_by_attribute_and_value(route)
        if not response or not response.get('users'):
            return None
        return User(**response.get('users')[0])

    def update(self, client, attribute, value, extra_data=None):
        route = f'users/{self.id}'
        response = client.update_by_id(route, attribute, value, extra_data)
        if not response:
            return None
        # actually sets the new attr in current memory too, not just api
        self.__dict__[attribute] = value
        return response.get('user')
    
    def save(self):
        pass
