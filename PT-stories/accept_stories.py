# The code below is from the AiDD conversation: https://eastagile.skydeck.ai/conversation/Hs1xVQWu888

import requests
import json
from datetime import datetime, timedelta

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

# Update story's accepted_at value to be within the same week as created_at
def update_story_accepted_at(story):
    created_at = datetime.fromisoformat(story['created_at'].replace('Z', '+00:00'))
    accepted_at = created_at + timedelta(days=3)  # Adding 3 days to keep it within the same week

    url = f"https://www.pivotaltracker.com/services/v5/projects/{PROJECT_ID}/stories/{story['id']}"
    body = {
        'accepted_at': accepted_at.isoformat()
    }

    updated_story = put_request(url, body)
    return updated_story

# Main script
def main():
    stories = fetch_all_accepted_stories()
    for story in stories:
        updated_story = update_story_accepted_at(story)
        print(f"Updated story {story['id']} accepted_at to {updated_story['accepted_at']}")

if __name__ == "__main__":
    main()
