from models.base import Base


class ProjectTemplate(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_project_template(cls, client, data):
        route = 'project_templates'
        response = client.create_new(route, data)
        if not response or not response.get('project_template'):
            return None
        project_template = ProjectTemplate(**response.get('project_template'))
        return project_template

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'project_templates'
        response = client.get_all(route, extra_data)
        if not response or not response.get('project_templates'):
            print(response, '**BAD RESPONSE**')
            return []
        return [ProjectTemplate(**project_template_dict) for project_template_dict in response.get('project_templates')]