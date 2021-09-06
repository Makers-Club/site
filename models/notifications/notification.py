from models.base import Base

class Notification(Base):

    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)

    def create(self, client):
        """ Ping API to create a notifciation """
        route = f'notifications'
        data = self.to_dict()
        response = client.create(route, extra_data=data)
        if response is None:
            raise Exception("(notification.py: 14) Error: Notification Creation failed")
        else:
            print(f"(notification.py: 17) Response: {response}")

    def mark_read(self, client, data=None):
        """ Ping API to update notification as read """
        response = client.update_by_id(f'notifications/{self.id}', 'is_read', True, data)
        if response is None:
            raise Exception("(notification.py: 22) Update Failed")

    def delete(self, client, data=None):
        """ Ping API to delete a notification """
        route = f'notifications/{self.id}'
        response = client.delete(route, data)
        if response is None:
            raise Exception("(notification.py: 29) Delete Failed")
    