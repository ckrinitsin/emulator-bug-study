from requests import get
from os import makedirs, path

def process_launchpad_bug(bug_id):
    if path.exists(f"output_launchpad/{bug_id}"):
        return

    bug_url = f"https://api.launchpad.net/1.0/bugs/{bug_id}"

    bug_response = get(url = bug_url)

    bug_data = bug_response.json()

    messages_response = get(url = bug_data['messages_collection_link'])

    messages_data = messages_response.json()

    makedirs("output_launchpad", exist_ok=True)
    with open(f"output_launchpad/{bug_id}", "w") as file:
        file.write(f"{bug_data['title']}\n\n")

        for entry in messages_data['entries']:
            file.write(f"{entry['content']}\n\n")

if __name__ == "__main__":
    process_launchpad_bug(1629282)
    process_launchpad_bug(1915063)
