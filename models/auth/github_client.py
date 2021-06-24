from requests import post, get
from re import search
from b import User
from models.auth.auth import Auth

class GithubClient:

    def __init__(self, auth_data):
        self.__auth_data = auth_data

    
    def get_user(self, gh_tmp_code):
        """receives github code, returns user and session"""
        
        gh_access_token = self.get_gh_access_token(gh_tmp_code)
        if gh_access_token is None:
            print('Github credentials are off or the code was fake')
            return None, None
        user_data = self.get_gh_user_data(gh_access_token)
        if user_data is None:
            # User has a Github account without any verified emails
            return None, None
        user = self.match_user(user_data)    
        session = Auth.login(gh_access_token, user.id)
        return user, session

    def get_gh_access_token(self, gh_tmp_code):
        """Exchanges a temporary code for an access token from Github API"""

        # Make POST request to Github Login OAuth Access Token URL
        oauth_url = 'https://github.com/login/oauth/access_token?'
        self.__auth_data['code'] = gh_tmp_code
        response = post(oauth_url, self.__auth_data)

        # Find and return access token using regex with capture group
        match = search('access_token=(.*?)(&|$)', response.text)
        if match is None:
            print(response.text)
            print(self.__auth_data)
            return None

        # match[0] is the full matched string ('access_token=...')
        # match[1] is the access token itself.
        return match[1]

    @staticmethod
    def get_gh_user_data(gh_access_token):
        """Uses a Github access token to retrieve user data"""

        headers = {
            'content-type': 'application/json',
            'Authorization': f'token {gh_access_token}'
        }

        gh_response = get('https://api.github.com/user', headers=headers)
        if gh_response.status_code != 200:
            print('Faulty response')
            return None
        
        user_data = gh_response.json()
        user_data['access_token'] = gh_access_token

        if user_data['email'] is None: # if user email is private, GET /user/emails too
            gh_response = get('https://api.github.com/user/emails', headers=headers)
            for email_dict in gh_response.json():
                if email_dict.get('primary') and email_dict.get('verified'):
                    user_data['email'] = email_dict.get('email')
                    return user_data
            return None

        return user_data

    @staticmethod
    def match_user(user_data):
        """matches user data with a user, returns user"""
        user = User.get_by_id(user_data['id'])

        # TODO: See Issue #66
        if user is None: # No user? Make new user!
            user = User(**user_data)
            user.save()
            print('NEW USER {} ADDED TO DATABASE'.format(user.id))
        else:
            # update user's access token to new value
            user.access_token = user_data['access_token']
            user.save()
        return user
