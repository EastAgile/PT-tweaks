# The code below is from the AiDD conversations:
# - https://eastagile.skydeck.ai/conversation/Hs1xVQWu888
# - https://eastagile.skydeck.ai/conversation/CONzSzwnBqc

import requests
import json
from datetime import datetime, timedelta, timezone

# Constants
TOKEN = 'your Pivotal Tracker API token'
PROJECT_ID = 'your Pivotal Tracker project ID'
STORIES_PER_PAGE = 100
HEADERS = {
    'X-TrackerToken': TOKEN,
    'Content-Type': 'application/json'
}

# Helper function to perform GET requests
def get_request(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Helper function to perform PUT requests
def put_request(url, body):
    response = requests.put(url, headers=HEADERS, data=json.dumps(body))
    response.raise_for_status()
    return response.json()

# Fetch all accepted stories with pagination
def fetch_all_accepted_stories():
    stories = []
    offset = 0

    while True:
        url = f"https://www.pivotaltracker.com/services/v5/projects/{PROJECT_ID}/stories?with_state=accepted&limit={STORIES_PER_PAGE}&offset={offset}"
        page_stories = get_request(url)
        stories.extend(page_stories)
        if len(page_stories) < STORIES_PER_PAGE:
            break
        offset += STORIES_PER_PAGE

    return stories

# Fetch story transitions to find when the story was started
def fetch_story_start_date(story_id):
    url = f"https://www.pivotaltracker.com/services/v5/projects/{PROJECT_ID}/stories/{story_id}/transitions"
    transitions = get_request(url)
    for transition in transitions:
        if transition['state'] == 'started':
            return datetime.fromisoformat(transition['occurred_at'].replace('Z', '+00:00'))
    return None

# Update story's accepted_at value to be within the same week as started_at
def update_story_accepted_at(story):
    created_at = datetime.fromisoformat(story['created_at'].replace('Z', '+00:00'))
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)

    if created_at < six_months_ago:
        print(f"Skipping story {story['id']} as it was created more than 6 months ago.")
        return

    started_at = fetch_story_start_date(story['id'])
    if started_at:
        accepted_at = started_at + timedelta(days=1)  # Adding 1 day to keep it within the same week

        # Check if the current accepted_at is already within the same week as started_at
        current_accepted_at = datetime.fromisoformat(story['accepted_at'].replace('Z', '+00:00'))
        if current_accepted_at.isocalendar()[:2] == started_at.isocalendar()[:2]:
            print(f"No need to update story {story['id']} as accepted_at is already in the same week as started_at.")
            return

        url = f"https://www.pivotaltracker.com/services/v5/projects/{PROJECT_ID}/stories/{story['id']}"
        body = {
            'accepted_at': accepted_at.isoformat()
        }

        updated_story = put_request(url, body)
        return updated_story
    else:
        print(f"Could not find started_at for story {story['id']}")
        return None

# Main script
def main():
    stories = fetch_all_accepted_stories()
    for story in stories:
        updated_story = update_story_accepted_at(story)
        if updated_story:
            print(f"Updated story {story['id']} accepted_at {story['accepted_at']} to {updated_story['accepted_at']}")

if __name__ == "__main__":
    main()
