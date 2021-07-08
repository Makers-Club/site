from models.base import Base


class Task(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_task(cls, client, data):
        route = 'tasks'
        response = client.create_new(route, data)
        if not response or not response.get('task'):
            return None
        task = Task(**response.get('task'))
        return task

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'tasks'
        response = client.get_all(route, extra_data)
        if not response or not response.get('tasks'):
            return []
        return [Task(**task_dict) for task_dict in response.get('tasks')]