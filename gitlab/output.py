from tomlkit import dumps
from os import path, makedirs

def find_label(labels : list, keyword : str) -> str:
    match = next((s for s in labels if f"{keyword}:" in s), None)
    if not match:
        return f"{keyword}_missing"
    return match.replace(": ", "_")

def write_file(file_path : str, string : str) -> None:
    makedirs(path.dirname(file_path), exist_ok = True)
    with open(file_path, "w") as file:
        file.write(string)

def output_issue(issue : dict) -> None:
    labels = issue['labels']
    issue_id = issue['id']
    toml_string = dumps(issue)

    target_label = find_label(labels, "target")
    host_label = find_label(labels, "host")
    accel_label = find_label(labels, "accel")
    write_file(f"issues/{target_label}/{host_label}/{accel_label}/{issue_id}.toml", toml_string)
