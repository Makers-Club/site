from models.base import Base


class Sprint(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_sprint(cls, client, data):
        route = 'sprints'
        response = client.create_new(route, data)
        if not response or not response.get('sprint'):
            return None
        sprint = Sprint(**response.get('sprint'))
        return sprint

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'sprints'
        response = client.get_all(route, extra_data)
        if not response or not response.get('sprints'):
            return []
        return [Sprint(**sprint_dict) for sprint_dict in response.get('sprints')]