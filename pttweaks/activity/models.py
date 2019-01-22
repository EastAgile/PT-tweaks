from .utils import utc_from_str


class DictModel(object):
    def __init__(self, data):
        self._origin = data


class Project(DictModel):
    @property
    def id(self):
        return self._origin['id']

    @property
    def iteration_length(self):
        return self._origin['iteration_length']

    @property
    def start_time(self):
        return utc_from_str(self._origin['start_time'])


class ActivityChange(DictModel):
    @property
    def id(self):
        return self._origin['id']

    @property
    def new_values(self):
        return self._origin['new_values']

    @property
    def change_type(self):
        return self._origin['change_type']

    def is_accept_activity(self):
        return self.change_type == 'update' and self.new_values.get('current_state', None) == 'accepted'


class Activity(DictModel):
    @property
    def project(self):
        return Project(self._origin['project'])

    @property
    def changes(self):
        return [ActivityChange(item) for item in self._origin['changes']]
