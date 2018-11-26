class Entity(object):

    def __init__(self, object_type, object_id):
        self.object_type = object_type
        self.object_id = object_id
        self.related_entities = []

    def _populate_object_info(self):
        pass
