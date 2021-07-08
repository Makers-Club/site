from models.base import Base


class SprintTemplate(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_sprint_template(cls, client, data):
        route = 'sprint_templates'
        response = client.create_new(route, data)
        if not response or not response.get('sprint_template'):
            return None
        sprint_template = SprintTemplate(**response.get('sprint_template'))
        return sprint_template

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'sprint_templates'
        response = client.get_all(route, extra_data)
        if not response or not response.get('sprint_templates'):
            return []
        return [SprintTemplate(**sprint_template_dict) for sprint_template_dict in response.get('sprint_templates')]