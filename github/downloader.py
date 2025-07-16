from requests import get, Response
from output import output_issue
from argparse import ArgumentParser

parser = ArgumentParser(prog='downloader.py')
parser.add_argument('-r', '--repository', required=True, help="Which repository to download the issues from")
args = parser.parse_args()

per_page = 100
url = f"https://api.github.com/repos/{args.repository}/issues?per_page={per_page}&state=all"
check_url = f"https://api.github.com/repos/{args.repository}"

def pages_iterator(first : Response):
    current = first
    while current.links.get('next'):
        current.raise_for_status()
        yield current
        current = get(url = current.links.get('next').get('url'))
    current.raise_for_status()
    yield current

def main():
    check = get(check_url)
    check.raise_for_status()

    for index, response in enumerate(pages_iterator(get(url))):
        print(f"Current page: {index+1}")

        data = response.json()
        for i in data:
            if "pull_request" in i:
                continue

            issue = {
                "id": i['number'],
                "title": i['title'],
                "labels": [label['name'] for label in i['labels']],
                "description": i['body'],
            }

            output_issue(issue)

if __name__ == "__main__":
    main()
