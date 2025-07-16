from os import path, makedirs

def write_file(file_path : str, string : str) -> None:
    makedirs(path.dirname(file_path), exist_ok = True)
    with open(file_path, "w") as file:
        file.write(string)

def output_issue(issue : dict) -> None:
    try:
        if 'documentation' in issue['labels']:
            write_file(f"issues/documentation/{issue['id']}", issue['title'] + '\n' + (issue['description'] or ""))
        else:
            write_file(f"issues/{issue['id']}", issue['title'] + '\n' + (issue['description'] or ""))
    except TypeError:
        print(f"error with bug {issue['id']}")
        exit()
