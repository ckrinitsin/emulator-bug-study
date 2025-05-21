from datetime import datetime, timedelta
from urllib.request import urlopen

from bs4 import BeautifulSoup
from re import search

end_date = datetime(2015, 4, 1)
# end_date = datetime.today().replace(day=1) #####
start_date = datetime.today().replace(day=1)

def months_iterator(start, end):
    current = start
    while current >= end:
        yield current
        if current.month == 1:
            current = current.replace(year=current.year - 1, month=12)
        else:
            current = current.replace(month=current.month - 1)

def main():
    count = 0
    for month in months_iterator(start = start_date, end = end_date):
        url = f"https://lists.nongnu.org/archive/html/qemu-devel/{month.strftime('%Y-%m')}/threads.html"

        html = urlopen(url).read()

        soup = BeautifulSoup(html, features='html5lib')

        ul = soup.body.ul
        threads = ul.find_all('li', recursive=False)
        for li in threads:
            a_tag = li.find('b').find('a')

            if not a_tag:
                continue

            text = a_tag.get_text(strip=True)
            href = a_tag.get('href')
            match = search(r'\[[^\]]*\b(BUG|bug|Bug)\b[^\]]*\]', text) # matches bug enclosed in []

            if not match:
                continue

            match = search(r'(Re\:|RE\:|re\:)', text) # matches bug enclosed in []

            if match:
                continue

            match = search(r'\[Bug\s\d+\]', text) # matches bug enclosed in []

            if match:
                continue

            print(f"Text: {text}, Href: {href}")
            count = count + 1

        print(f"{month.strftime('%Y-%m')}, Count: {count}")

if __name__ == "__main__":
    main()
