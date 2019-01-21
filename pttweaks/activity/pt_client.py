from requests import request


class PTClient(object):
    base_url = 'https://www.pivotaltracker.com/services/v5/'

    def __init__(self, token):
        self.token = token

    def _make_request(self, url, method, **kwargs):
        headers = {
            'content-type': 'application/json',
            'X-TrackerToken': self.token
        }

        response = request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_story_activities(self, project_id, story_id):
        url = '{base_url}projects/{project_id}/stories/{story_id}/activity'.format(
            base_url=self.base_url,
            project_id=project_id,
            story_id=story_id,
        )

        return self._make_request(url, 'get')

    def update_story(self, project_id, story_id, **kwargs):
        url = '{base_url}projects/{project_id}/stories/{story_id}'.format(
            base_url=self.base_url,
            project_id=project_id,
            story_id=story_id
        )

        return self._make_request(url, 'put', json=kwargs)

    def get_project(self, project_id):
        url = '{base_url}projects/{project_id}'.format(
            base_url=self.base_url,
            project_id=project_id,
        )

        return self._make_request(url, 'get')
