from models.base import Base


class LearningResource(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_new_learning_resource(cls, client, data=None):
        route = 'learning_resources'
        response = client.create_new(route, data)
        if not response or not response.get('learning_resource'):
            return None
        learning_resource = LearningResource(**response.get('learning_resource'))
        return learning_resource

    @classmethod
    def get_all(cls, client, extra_data=None) -> list:
        route = 'learning_resources'
        response = client.get_all(route, extra_data)
        if not response or not response.get('learning_resources'):
            return []
        return [LearningResource(**learning_resource_dict) for learning_resource_dict in response.get('learning_resources')]