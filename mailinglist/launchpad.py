from requests import get, Response
from os import makedirs, path

def launchpad_id_valid(bug_id : str) -> bool:
    return len(bug_id) == 7 or len(bug_id) == 6

def response_valid(response : Response) -> bool:
    return 'application/json' in response.headers.get('Content-Type', '')

def process_launchpad_bug(bug_id : str) -> None:
    if not launchpad_id_valid(bug_id):
        print(f"{bug_id} is not valid")
        return

    if path.exists(f"output_launchpad/{bug_id}"):
        print(f"output_launchpad/{bug_id} exists already")
        return

    bug_url = f"https://api.launchpad.net/1.0/bugs/{bug_id}"
    bug_response = get(bug_url)

    if not response_valid(bug_response):
        print(f"Response for {bug_id} is not valid")
        return

    bug_data = bug_response.json()
    messages_response = get(bug_data['messages_collection_link'])
    messages_data = messages_response.json()

    makedirs("output_launchpad", exist_ok = True)
    with open(f"output_launchpad/{bug_id}", "w") as file:
        file.write(f"{bug_data['title']}\n\n")
        for entry in messages_data['entries']:
            file.write(f"{entry['content']}\n\n")
