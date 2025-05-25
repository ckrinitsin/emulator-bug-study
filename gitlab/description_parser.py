from re import sub, search, DOTALL
from tomlkit import string

def remove_comments(description : str) -> str:
    return sub(r'<!--(.|\n)*?-->', '', description)

def get_headline_content(description : str, headline : str) -> str:
    pattern = rf'## {headline}\s+(.*?)(?=##\s|\Z)'

    match = search(pattern, description, DOTALL)
    if match:
        return string(match.group(1).strip(), multiline = True)
    else:
        return "n/a"

def get_bullet_point(description : str, headline : str, category : str) -> str:
    pattern = rf'{headline}(?:(?:.|\n)+?){category}:\s+(?:`)?(.+?)(?:`)?(?=\s)(?:\n|$)'

    match = search(pattern, description)
    if match:
        return match.group(1).strip()
    else:
        return "n/a"

def parse_description(description : str) -> dict:
    desc = remove_comments(description)

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
