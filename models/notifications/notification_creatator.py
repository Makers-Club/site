from models.notifications.notification import Notification
from models.notifications.notification_types import types
from uuid import uuid4
from base64 import b64encode

def encode(message):
    message_bytes = message.encode('ascii')
    base64_bytes = b64encode(message_bytes)
    return base64_bytes.decode('ascii')

def notification_creator(notification_type, data):
    """ 
        Takes a notification type and creates a new notification to save to the database 
        
        notification_type: type of notification
        data: necessary data to create a notification
    """

    if notification_type is None:
        raise Exception('(notification_creator.py: 15) Error: No type given')

    if notification_type not in types.keys():
        raise Exception('(notification_creator.py: 18) Error: Invalid type')

    message = data.msg if hasattr(data, 'msg') else set_message(notification_type, data)

    content = {
        "id": data.id if hasattr(data, 'id') else uuid4(),
        "user_id": data.user_id,
        "msg": message,
        "is_read": data.is_read if hasattr(data, 'is_read') else False
    }

    notification = Notification(content)

    if notification is None:
        raise Exception("(notification_creator.py: 40) Notification Creation failed")

    return notification


def set_message(notification_type, data):
    if notification_type == types["SEND_INVITE"]:
        message = send_invite(data)

    if notification_type == types["RESPOND"]:
        message = respond(data)

    if notification_type == types["FEEDBACK"]:
        message = feedback(data)

    return message


def send_invite(data):
    """ create a message for sending an invite notification """
    invitor_handle = data['invitor_handle']    
    # project_id = data['project_id']

    invitor_link = f"<a href='https://api.makerteams.org/users/{invitor_handle}' target='_blank'>{invitor_handle}</a>"
    project_link = f"<a href='https://www.google.com' target='_blank'>link</a>"

    return encode(f"<p>{invitor_link} has invited you to work on a project: {project_link}</p>")


def respond(data):
    """ create a message for a responding notification """
    raise NotImplementedError


def feedback(data):
    """ create a message for feedback notification """
    raise NotImplementedError
