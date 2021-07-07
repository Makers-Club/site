from models.base import Base


class Session(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def create_new(cls, client, token, user_id, data=None):
        import requests
        route = 'sessions'
        url = f'{client.url}/{route}/{token}/{user_id}?token=123123'
        response = requests.post(url).json()
        print(response, 'RESPONSE')
        if not response or not response.get('session'):
            return None
        session = Session(**response.get('session'))
        return session

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'sessions'
        response = client.get_all(route, extra_data)
        if not response or not response.get('sessions'):
            return []
        return [Session(**session_dict) for session_dict in response.get('sessions')]
    
    @classmethod
    def get_user_from_cookie(cls, client, id, extra_data=None) -> dict:
        route = f'sessions/{id}'
        response = client.get_one(route, extra_data)
        if not response or not response.get('user'):
            return None
        from models.user import User
        user = User(**response.get('user'))
        return user



# HEYYY DO THIISSSS
    @classmethod
    def delete_by_user_id(cls, client, user_id, extra_data=None) -> dict:
        route = f'sessions/{user_id}'
        response = client.delete(route, extra_data)
        if not response or not response.get('status') == 'OK':
            return False
        return True
    

