from requests import get
from os import makedirs
from re import search, DOTALL, compile
from urllib.parse import urljoin

from bs4 import BeautifulSoup

def write_message(html, hash_value):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    with open(f"output_mailinglist/{hash_value}", "a") as file:
        file.write(f"{text}\n\n")

def process_thread(url, hash_value):
    request = get(url)
    text = request.text

    match = search(r'<!--X-Body-of-Message-->(.*?)<!--X-Body-of-Message-End-->', text, DOTALL)
    if match:
        write_message(match.group(1).strip(), hash_value)

    pattern = href_pattern = compile(r'\[<a\s+href="([^"]+)">Next in Thread</a>\]')
    for line in text.splitlines():
        if "Next in Thread" in line:
            match = pattern.search(line)
            if match:
                href = match.group(1)
                process_thread(urljoin(url, href), hash_value)

if __name__ == "__main__":
    makedirs("output_mailinglist", exist_ok=True)
    process_thread("https://lists.nongnu.org/archive/html/qemu-devel/2025-04/msg05446.html", 861041)
