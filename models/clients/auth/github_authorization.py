from models.user import User
from os import getenv



class GithubAuthorization():
    data = {
        'client_id': getenv('GITHUB_CLIENT_ID'),
        'client_secret': getenv('GITHUB_CLIENT_SECRET'),
        'redirect_uri': getenv('GITHUB_CALLBACK_URL'),
        'scope': ['read:user', 'user:email']
    }
    if getenv('PRODUCTION'):
        data['redirect_uri'] = 'https://makerteams.org/auth/github_callback'
    access_token_url = getenv('GITHUB_ACCESS_TOKEN_URL')
    
    def __init__(self):
        self.authorization_url = self.build_authorization_endpoint()
    

    def build_authorization_endpoint(self):
        parameters = {
            'client_id': self.data.get('client_id'),
            'scope': f'%20{self.data.get("scope")}'
        }
        auth_url = getenv('GITHUB_AUTH_URL')
        for k, v in parameters.items():
            auth_url += '{}={}&'.format(k, v)
        # print("\n\nAUTH URL", auth_url)
        return auth_url


    @classmethod
    def user(cls, request):
        code = request.args.get('code')
        if not code:
            return None
        token = cls.get_token_from(code)
        #print("\n\nTOKEN", token)
        if not token:
            return None
        user = cls.get_user_from(token)
        #print("\n\nUSER", user)
        return user

    @classmethod
    def get_token_from(cls, code):
        cls.data['code'] = code
        from models.clients.github_client import GithubClient
        return GithubClient.authorization_token(cls.access_token_url, cls.data)

    @classmethod
    def get_user_from(cls, token):
        import requests
        headers = {
            'content-type': 'application/json',
            'Authorization': f'token {token}'
        }
        user = requests.get('https://api.github.com/user', headers=headers)
        if user.status_code != 200:
            return None
        user = user.json()
        user['access_token'] = token
        return user

