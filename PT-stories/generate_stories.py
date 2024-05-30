# The code below is from the AiDD conversation: https://eastagile.skydeck.ai/conversation/8kqURLO76eX

import csv
import random
from datetime import datetime, timedelta

# Constants
titles = [f"Story {i+1}" for i in range(500)]
types = ['feature']
initial_labels = ['label1', 'label2', 'label3', 'label4', 'label5', 'label6', 'label7']
general_states = ['unscheduled', 'unstarted', 'started', 'finished', 'delivered', 'accepted', 'rejected']
chore_states = ['unscheduled', 'unstarted', 'started', 'accepted']
release_states = ['unscheduled', 'unstarted', 'accepted']
users = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Dave Wilson', 'Eve Davis', 'Fiona Clark', 'George Hall', 'Hannah King', 'Isaac Lee', 'Jack Harris']
point_scale = [1, 2, 3]

# Helper Functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

end_date = datetime.today()
start_date = end_date - timedelta(days=180)  # 6 months ago

# Track labels used for epics
used_epic_labels = set()
all_labels = initial_labels.copy()

def generate_new_label():
    base_label = "label"
    index = len(all_labels) + 1
    new_label = f"{base_label}{index}"
    all_labels.append(new_label)
    return new_label

# Counters for limiting epics, releases, chores, and bugs
epic_count = 0
release_count = 0
chore_count = 0
bug_count = 0
max_epics = 20
max_releases = 10
max_chores = 30
max_bugs = 70

# Open CSV file
with open('sample_stories.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Type', 'Description', 'Labels', 'Estimate', 'Current State', 'Created at', 'Accepted at', 'Requested By', 'Owned By', 'Comment'])

    for i in range(500):
        title = titles[i]

        # Determine story type based on remaining quotas
        if epic_count < max_epics and release_count < max_releases and chore_count < max_chores and bug_count < max_bugs:
            story_type = random.choice(types + ['epic', 'release', 'chore', 'bug'])
        elif epic_count < max_epics and release_count < max_releases and chore_count < max_chores:
            story_type = random.choice(types + ['epic', 'release', 'chore'])
        elif epic_count < max_epics and release_count < max_releases and bug_count < max_bugs:
            story_type = random.choice(types + ['epic', 'release', 'bug'])
        elif epic_count < max_epics and chore_count < max_chores and bug_count < max_bugs:
            story_type = random.choice(types + ['epic', 'chore', 'bug'])
        elif release_count < max_releases and chore_count < max_chores and bug_count < max_bugs:
            story_type = random.choice(types + ['release', 'chore', 'bug'])
        elif epic_count < max_epics and release_count < max_releases:
            story_type = random.choice(types + ['epic', 'release'])
        elif epic_count < max_epics and chore_count < max_chores:
            story_type = random.choice(types + ['epic', 'chore'])
        elif epic_count < max_epics and bug_count < max_bugs:
            story_type = random.choice(types + ['epic', 'bug'])
        elif release_count < max_releases and chore_count < max_chores:
            story_type = random.choice(types + ['release', 'chore'])
        elif release_count < max_releases and bug_count < max_bugs:
            story_type = random.choice(types + ['release', 'bug'])
        elif chore_count < max_chores and bug_count < max_bugs:
            story_type = random.choice(types + ['chore', 'bug'])
        elif epic_count < max_epics:
            story_type = 'epic'
        elif release_count < max_releases:
            story_type = 'release'
        elif chore_count < max_chores:
            story_type = 'chore'
        elif bug_count < max_bugs:
            story_type = 'bug'
        else:
            story_type = 'feature'

        description = f"Description for {title.lower()}"

        # Ensure unique labels for epics
        if story_type == 'epic':
            available_labels = [label for label in all_labels if label not in used_epic_labels]
            if not available_labels:
                label = generate_new_label()
            else:
                label = random.choice(available_labels)
            used_epic_labels.add(label)
            epic_count += 1
        else:
            label = random.choice(all_labels)

        # Ensure estimate is set correctly
        if story_type == 'feature':
            estimate = random.choice(point_scale)
        else:
            estimate = ''

        # Set current state based on story type
        if story_type == 'chore':
            state = random.choice(chore_states)
            chore_count += 1
        elif story_type == 'release':
            state = random.choice(release_states)
            release_count += 1
        elif story_type == 'bug':
            state = random.choice(general_states)
            bug_count += 1
        else:
            state = random.choice(general_states)

        created_at = random_date(start_date, end_date).strftime("%Y-%m-%d")
        accepted_at = random_date(datetime.strptime(created_at, "%Y-%m-%d"), end_date).strftime("%Y-%m-%d") if state == 'accepted' else ''

        requested_by = random.choice(users)
        owned_by = random.choice(users)
        comment = f"comment{i+1}"

        writer.writerow([title, story_type, description, label, estimate, state, created_at, accepted_at, requested_by, owned_by, comment])