# The code below is from the AiDD conversation:
# - https://eastagile.skydeck.ai/conversation/8kqURLO76eX
# - https://eastagile.skydeck.ai/conversations/17835

import csv
import random
from datetime import datetime, timedelta

# Constants
titles = [f"Story {i + 1}" for i in range(500)]
types = ['feature']
initial_labels = ['label1', 'label2', 'label3', 'label4', 'label5', 'label6', 'label7']
general_states = ['unscheduled', 'unstarted', 'started', 'finished', 'delivered', 'accepted', 'rejected']
chore_states = ['unscheduled', 'unstarted', 'started', 'accepted']
release_states = ['unscheduled', 'unstarted', 'accepted']
users = [
    'Alice Johnson',
    'Bob Smith',
    'Charlie Brown',
    'Dave Wilson',
    'Eve Davis',
    'Fiona Clark',
    'George Hall',
    'Hannah King',
    'Isaac Lee',
    'Jack Harris'
]
point_scale = [1, 2, 3]

# Helper Functions


def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))


def generate_new_label(all_labels):
    base_label = "label"
    index = len(all_labels) + 1
    new_label = f"{base_label}{index}"
    all_labels.append(new_label)
    return new_label


def select_story_type(epic_count, release_count, chore_count, bug_count, max_epics, max_releases, max_chores, max_bugs):
    available_types = types + ['epic', 'release', 'chore', 'bug']

    if epic_count >= max_epics:
        available_types.remove('epic')
    if release_count >= max_releases:
        available_types.remove('release')
    if chore_count >= max_chores:
        available_types.remove('chore')
    if bug_count >= max_bugs:
        available_types.remove('bug')

    return random.choice(available_types)


def get_unique_label(story_type, all_labels, used_epic_labels):
    if story_type == 'epic':
        available_labels = [label for label in all_labels if label not in used_epic_labels]
        if not available_labels:
            label = generate_new_label(all_labels)
        else:
            label = random.choice(available_labels)
        used_epic_labels.add(label)
    else:
        label = random.choice(all_labels)
    return label


def get_estimate(story_type, point_scale):
    return random.choice(point_scale) if story_type == 'feature' else ''


def get_state(story_type, chore_states, release_states, general_states):
    if story_type == 'chore':
        return random.choice(chore_states)
    elif story_type == 'release':
        return random.choice(release_states)
    elif story_type == 'bug':
        return random.choice(general_states)
    else:
        return random.choice(general_states)


def generate_csv(
        titles, all_labels, used_epic_labels, max_epics, max_releases, max_chores, max_bugs,
        point_scale, chore_states, release_states, general_states, start_date, end_date, users):

    epic_count = release_count = chore_count = bug_count = 0

    with open('sample_stories.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Type', 'Description', 'Labels', 'Estimate', 'Current State',
                         'Created at', 'Accepted at', 'Requested By', 'Owned By', 'Comment'])

        for i in range(500):
            title = titles[i]
            story_type = select_story_type(
                epic_count,
                release_count,
                chore_count,
                bug_count,
                max_epics,
                max_releases,
                max_chores,
                max_bugs)
            description = f"Description for {title.lower()}"
            label = get_unique_label(story_type, all_labels, used_epic_labels)
            estimate = get_estimate(story_type, point_scale)
            state = get_state(story_type, chore_states, release_states, general_states)

            if story_type == 'epic':
                epic_count += 1
            elif story_type == 'release':
                release_count += 1
            elif story_type == 'chore':
                chore_count += 1
            elif story_type == 'bug':
                bug_count += 1

            created_at = random_date(start_date, end_date).strftime("%Y-%m-%d")
            accepted_at = (random_date(datetime.strptime(created_at, "%Y-%m-%d"), end_date).strftime("%Y-%m-%d")
                           if state == 'accepted' else '')

            requested_by = random.choice(users)
            owned_by = random.choice(users)
            comment = f"comment{i + 1}"

            writer.writerow([title, story_type, description, label, estimate, state,
                             created_at, accepted_at, requested_by, owned_by, comment])


# Main Execution
end_date = datetime.today()
start_date = end_date - timedelta(days=180)  # 6 months ago
used_epic_labels = set()
all_labels = initial_labels.copy()

generate_csv(
    titles, all_labels, used_epic_labels, 20, 10, 30, 70, point_scale,
    chore_states, release_states, general_states, start_date, end_date, users
)
