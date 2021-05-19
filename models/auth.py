from models.user import User

class Auth():
    def __init__(self):
        pass

    @classmethod
    def register(cls, user):
        ''' register a new user '''
        if not type(user) == User:
            raise TypeError
        user.save()
        return user