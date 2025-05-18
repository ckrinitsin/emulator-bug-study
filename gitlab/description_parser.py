import re
from tomlkit import string

def remove_comments(description):
    return re.sub(r'<!--(.|\n)*?-->', '', description)

def get_headline_content(description, headline):
    pattern = rf'## {headline}\s+(.*?)(?=##\s|\Z)'

    match = re.search(pattern, description, re.DOTALL)
    if match:
        return string(match.group(1).strip(), multiline=True)
    else:
        return "n/a"

def get_bullet_point(description, headline, category):
    pattern = rf'{headline}(?:(?:.|\n)+?){category}:\s+(?:`)?(.+?)(?:`)?(?=\s)(?:\n|$)'

    match = re.search(pattern, description)
    if match:
        return match.group(1).strip()
    else:
        return "n/a"

def parse_description(desc):
    desc = remove_comments(desc)

    result = {
        "host-os": get_bullet_point(desc, "Host", "Operating system"),
        "host-arch": get_bullet_point(desc, "Host", "Architecture"),
        "qemu-version": get_bullet_point(desc, "Host", "QEMU version"),
        "guest-os": get_bullet_point(desc, "Emulated", "Operating system"),
        "guest-arch": get_bullet_point(desc, "Emulated", "Architecture"),
        "description": get_headline_content(desc, "Description of problem"),
        "reproduce": get_headline_content(desc, "Steps to reproduce"),
        "additional": get_headline_content(desc, "Additional information")
    }

    return result
