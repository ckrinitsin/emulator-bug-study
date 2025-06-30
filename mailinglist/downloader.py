from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urljoin
from os import makedirs, path
from shutil import rmtree
from re import search, match

from bs4 import BeautifulSoup

from launchpad import process_launchpad_bug
from thread import process_thread

start_date = datetime(2015, 4, 1)
end_date = datetime(2025, 5, 1)

def months_iterator(start, end):
    current = start
    while current <= end:
        yield current
        if current.month == 12:
            current = current.replace(year = current.year + 1, month = 1)
        else:
            current = current.replace(month = current.month + 1)

def prepare_output() -> None:
    if path.exists("output_mailinglist"):
        rmtree("output_mailinglist")
    if path.exists("output_launchpad"):
        rmtree("output_launchpad")
    makedirs("output_mailinglist", exist_ok = True)

def is_bug(text : str) -> bool:
    return search(r'\[[^\]]*\b(BUG|bug|Bug)\b[^\]]*\]', text) # matches bug enclosed in []

def main():
    prepare_output()

    for month in months_iterator(start_date, end_date):
        print(f"{month.strftime('%Y-%m')}")
        url = f"https://lists.nongnu.org/archive/html/qemu-devel/{month.strftime('%Y-%m')}/threads.html"
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features = 'html5lib')

        ul = soup.body.ul
        threads = ul.find_all('li', recursive = False)
        for li in reversed(threads):
            a_tag = li.find('b').find('a')
            if not a_tag:
                continue

            text = a_tag.get_text(strip = True)
            href = a_tag.get('href')

            if not is_bug(text):
                continue

            # bug issued in launchpad
            re_match = search(r'\[Bug\s(\d+)\]', text) # matches [Bug <number>]
            if re_match:
                process_launchpad_bug(re_match.group(1).strip())
                continue

            # existing thread
            re_match = match(r'(?i)^re:\s*(.*)', text) # matches 'Re:'
            if re_match:
                title_hash = str(hash(re_match.group(1).strip()))[1:9]
                if path.exists(f"output_mailinglist/{title_hash}"):
                    process_thread(urljoin(url, href), title_hash)
                continue

            # new thread
            title_hash = str(hash(text.strip()))[1:9]
            if path.exists(f"output_mailinglist/{title_hash}"):
                print(f"ERROR: {title_hash} should not exist!")
                continue

            with open(f"output_mailinglist/{title_hash}", "w") as file:
                file.write(f"{text}\n\n")
            process_thread(urljoin(url, href), title_hash)

if __name__ == "__main__":
    main()
