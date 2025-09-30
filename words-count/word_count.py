from os import path, listdir, makedirs

paths = [ "../results/scraper/box64", "../results/scraper/launchpad-without-comments", "../results/scraper/mailinglist", "../results/scraper/gitlab/issues_text" ]
paths = [ "../results/scraper/launchpad-without-comments", "../results/scraper/mailinglist", "../results/scraper/gitlab/issues_text" ]

def list_files_recursive(directory, basename = False):
    result = []
    if not path.isdir(directory):
        return result
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

def main():
    files = []
    for path in paths:
        new_files = list_files_recursive(path)
        print(f"{path} has {len(new_files)} reports")
        files = files + list_files_recursive(path)

    bug_count = len(files)

    word_count = 0
    for path in files:
        with open(path, "r") as file:
            words = len(file.read().split(" "))
            word_count = word_count + words

    avg_word_per_bug = word_count / bug_count
    print(f"Average word per report count: {avg_word_per_bug}")

if __name__ == "__main__":
    main()
