from models.base import Base


class TaskTemplate(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_task_template(cls, client, data):
        route = 'task_templates'
        response = client.create_new(route, data)
        if not response or not response.get('task_template'):
            return None
        task_template = TaskTemplate(**response.get('task_template'))
        return task_template

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'task_templates'
        response = client.get_all(route, extra_data)
        if not response or not response.get('task_templates'):
            return []
        return [TaskTemplate(**task_template_dict) for task_template_dict in response.get('task_templates')]