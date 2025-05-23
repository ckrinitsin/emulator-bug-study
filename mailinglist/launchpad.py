from requests import get
from os import makedirs, path

def process_launchpad_bug(bug_id) -> bool:
    if path.exists(f"output_launchpad/{bug_id}"):
        return false

    bug_url = f"https://api.launchpad.net/1.0/bugs/{bug_id}"

    bug_response = get(url = bug_url)

    if not 'application/json' in bug_response.headers.get('Content-Type', ''):
        return false

    bug_data = bug_response.json()

    messages_response = get(url = bug_data['messages_collection_link'])

    messages_data = messages_response.json()

    makedirs("output_launchpad", exist_ok=True)
    with open(f"output_launchpad/{bug_id}", "w") as file:
        file.write(f"{bug_data['title']}\n\n")

        for entry in messages_data['entries']:
            file.write(f"{entry['content']}\n\n")
    return true
