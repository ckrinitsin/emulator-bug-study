from requests import get
from json import dumps

project_id = 11167699
per_page = 100
url = f"https://gitlab.com/api/v4/projects/{project_id}/issues?per_page={per_page}"

def pages_iterator(first):
    current = first
    while current.links.get('next'):
        current.raise_for_status()
        yield current
        current = get(url = current.links.get('next').get('url'))
    current.raise_for_status()
    yield current

def main():
    for response in pages_iterator(get(url = url)):
        print(f"Current page: {response.headers['x-page']}")

        data = response.json()
        for i in data:

            issue = {
                "id": i['iid'],
                "title": i['title'],
                "state": i['state'],
                "description": i['description'],
                "created_at": i['created_at'],
                "closed_at": i['closed_at'],
                "labels": i['labels'],
                "url": i['web_url']
            }

            json_string = dumps(obj = issue, indent = 2)
            print(json_string)

if __name__ == "__main__":
    main()
