from .models import StatsModel

class StatsService:
    def __init__(self):
        self.model = StatsModel()
    
    def create(self, params):
        return self.model.add_application(params)
    
    def delete(self, id):
        return self.model.delete_application(id)
    
    def get_applications(self, user_id):
        return self.model.get_by_user_id(user_id)
    
    def get_response_types(self):
        return self.model.get_response_types()