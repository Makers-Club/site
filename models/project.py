from models.base import Base


class Project(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_project(cls, client, data):
        route = 'projects'
        response = client.create_new(route, data)
        if not response or not response.get('project'):
            return None
        project = Project(**response.get('project'))
        return project

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'projects'
        response = client.get_all(route, extra_data)
        if not response or not response.get('projects'):
            return []
        return [Project(**project_dict) for project_dict in response.get('projects')]
    
    def delete(self, client):
        route = f'projects/{self.id}'
        response = client.delete(route)
        if not response or not response.get('status') == 'OK':
            return False
        return True
    
    @classmethod
    def get_by_id(cls, client, id, extra_data=None) -> dict:
        route = f'projects/{id}'
        response = client.get_one(route, extra_data)
        if not response or not response.get('project'):
            return None
        project = Project(**response.get('project'))
        return project