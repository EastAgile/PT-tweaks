class DictModel(object):
    def __init__(self, data):
        self._origin = data


class Project(DictModel):
    @property
    def id(self):
        return self._origin['id']


class ActivityChange(DictModel):
    @property
    def id(self):
        return self._origin['id']

    @property
    def new_values(self):
        return self._origin['new_values']

    def is_accept_activity(self):
        return self.new_values.get('current_state', None) == 'accepted'


class Activity(DictModel):
    @property
    def project(self):
        return Project(self._origin['project'])

    @property
    def changes(self):
        return [ActivityChange(item) for item in self._origin['changes']]
