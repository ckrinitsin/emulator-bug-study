from argparse import ArgumentParser
from os import path, listdir, makedirs

parser = ArgumentParser()

parser.add_argument('-b', '--bugs', required = True)
parser.add_argument('-d', '--search_directory', required = True)
parser.add_argument('-o', '--output')

args = parser.parse_args()

def list_files_recursive(directory, basename = False):
    result = []
    for entry in listdir(directory):
        full_path = path.join(directory, entry)
        if path.isdir(full_path):
            result = result + list_files_recursive(full_path, basename)
        else:
            if basename:
                result.append(path.basename(full_path))
            else:
                result.append(full_path)
    return result

def output_csv(dictionary, full_path):
    with open(path.join(full_path, 'analysis.csv'), "w") as file:
        file.write("category, count\n")
        for key, value in dictionary.items():
            file.write(f"{key}, {value}\n")

def duplicate_bug(file_path, category):
    output_path = path.join(args.output, category)
    makedirs(output_path, exist_ok = True)
    with open(file_path, "r") as file:
        text = file.read()
    with open(path.join(output_path, path.basename(file_path)), "w") as file:
        file.write(text)

def main():
    result = {}
    mistranslation_bugs = list_files_recursive(args.bugs, True)
    bugs = list_files_recursive(args.search_directory, False)

    for mistranslation_bug in mistranslation_bugs:
        for bug in bugs:
            if mistranslation_bug == path.basename(bug):
                category = path.basename(path.dirname(bug))
                if args.output:
                    duplicate_bug(bug, category)
                if category in result:
                    result[category] += 1
                else:
                    result[category] = 1
                continue

    output_csv(result, args.search_directory)

if __name__ == "__main__":
    main()
