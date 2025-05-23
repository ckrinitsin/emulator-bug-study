from datetime import datetime, timedelta
from urllib.request import urlopen
from os import makedirs, path, remove
from shutil import rmtree
from re import search, match
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from launchpad import process_launchpad_bug
from thread import process_thread

start_date = datetime(2015, 4, 1)
end_date = datetime.today().replace(day=1)

def months_iterator(start, end):
    current = start
    while current <= end:
        yield current
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

def main():
    if path.exists("output_mailinglist"):
        rmtree("output_mailinglist")

    if path.exists("output_launchpad"):
        rmtree("output_launchpad")

    makedirs("output_mailinglist", exist_ok=True)
    for month in months_iterator(start = start_date, end = end_date):
        print(f"{month.strftime('%Y-%m')}")
        url = f"https://lists.nongnu.org/archive/html/qemu-devel/{month.strftime('%Y-%m')}/threads.html"

        html = urlopen(url).read()

        soup = BeautifulSoup(html, features='html5lib')

        ul = soup.body.ul
        threads = ul.find_all('li', recursive=False)
        for li in reversed(threads):
            a_tag = li.find('b').find('a')

            if not a_tag:
                continue

            text = a_tag.get_text(strip=True)
            href = a_tag.get('href')

            re_match = search(r'\[[^\]]*\b(BUG|bug|Bug)\b[^\]]*\]', text) # matches bug enclosed in []
            if not re_match:
                continue

            re_match = search(r'\[Bug\s(\d+)\]', text) # matches [Bug <number>] if bug is issued in launchpad
            if re_match:
                if not process_launchpad_bug(re_match.group(1).strip()):
                    print(f"Could not parse launchpad bug with id: {re_match.group(1).strip()}")
                continue

            re_match = match(r'(?i)^re:\s*(.*)', text) # matches 'Re:', meaning it's not a new thread
            if re_match:
                title_hash = hash(re_match.group(1).strip()) % 1000000
                if path.exists(f"output_mailinglist/{title_hash}"):
                    process_thread(urljoin(url, href), title_hash)
                continue

            title_hash = hash(text.strip()) % 1000000
            if path.exists(f"output_mailinglist/{title_hash}"):
                print(f"ERROR: {title_hash} should not exist!")
                continue

            with open(f"output_mailinglist/{title_hash}", "w") as file:
                file.write(f"{text}\n\n")
            process_thread(urljoin(url, href), title_hash)

if __name__ == "__main__":
    main()
