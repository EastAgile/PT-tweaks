# PT tweaks
Pivotal Tracker still has a flaw with the way the timing of stories is allocated when they are `finally` accepted. As we all know, the `Product Owner` often accepts stories long after their work has been finished and they have been delivered.

The problem that results from this is that stories look `done` only when they are `accepted`. And this means stories are not taken to account until some rather arbitrary time in the future. This results affects the `velocity measurements` and makes the misleading impression on the performance of the team.

To solve this issue, this application will watch user's activities on Pivotal Tracker and adjusts stories so that their `accepted date` is set to their last `delivered date` or `finished date`.

Pivotal Tracker document stated that updating `Accepted date` do not update the `Story Composition Report` (https://www.pivotaltracker.com/help/articles/updating_accepted_stories/). However, it should still works normally in our case.

# Getting started
## Requirements

- Python >3.6
- Django ~2.1


## Development
1 - Install dependencies for development:
```shell
$ pip install -r requirements/local.txt
```
To expose our webhook to Pivotal Tracker API we need to install [ngrok](https://ngrok.com/)

2 - Update `.env` file follow `.env.sample` file

3 - Start application
```shell
manage.py runserver 0.0.0.0:8000
ngrok http 8000
```

4 - Copy webhook url `https://<ngrok-url>/activity/webhook/<webhook_verify_token>/`
and [add to PT project webhook](https://www.pivotaltracker.com/help/articles/activity_webhook/#to-set-up-an-project-webhook-in-tracker)

5 - [Get Pivotal Tracker Token API](https://www.pivotaltracker.com/help/articles/api_token/) and update the env `PIVOTALTRACKER_TOKEN_API`

## Deploy production
1 - Install dependencies for production:
```shell
$ pip install -r requirements/base.txt
```
2 - [Deploy application to server]() (enable https)

3 - Update the enviroment variables.

4 - Add webhook url to PT project.

## Testing
1 - Install dependencies:
```shell
$ pip install -r requirements/test.txt
```

To run unit tests
```shell
$ manage.py test
```

Check the coverage:
```shell
$ coverage run manage.py test
$ coverage html
$ coverage report
```

Linting using flake8:
```shell
$ flake8 .
```

# Known issues
- PT has a [limit on story activity changes history](https://www.pivotaltracker.com/help/api/rest/v5#Activity)(limited to most recent 6 months), so if the story is too old, we won't have changes history to adjust accepted date.
