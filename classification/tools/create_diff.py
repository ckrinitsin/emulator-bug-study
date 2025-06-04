from os import path, walk
from pathlib import Path
from argparse import ArgumentParser

root_directory = "../../results/classifier/"

parser = ArgumentParser(prog='create_diff.py')
parser.add_argument('old')
parser.add_argument('new')
args = parser.parse_args()

def find_changes(old_directory, new_directory):
    old_files = {}
    for root, dirs, files in walk(old_directory):
        for file in files:
            relative_path = Path(root).relative_to(old_directory)
            old_files[file] = str(relative_path)

    new_files = {}
    for root, dirs, files in walk(new_directory):
        for file in files:
            relative_path = Path(root).relative_to(new_directory)
            new_files[file] = str(relative_path)

    changed_files = []
    for file in old_files:
        if file in new_files and old_files[file] != new_files[file]:
            changed_files.append({
                'name': file,
                'old': old_files[file],
                'new': new_files[file]
            })

    return changed_files

def output_diff(changed_files):
    with open(path.join(root_directory, args.new, f"{args.old}-{args.new}"), "w") as file:
        file.write(f"{len(changed_files)} changes:\n")
        for change in changed_files:
            file.write(f"{change['name']}: {change['old']} -> {change['new']}\n")

def main():
    path_old = path.join(root_directory, args.old)
    path_new = path.join(root_directory, args.new)

    result = find_changes(path_old, path_new)
    output_diff(result)

if __name__ == "__main__":
    main()
