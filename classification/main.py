from transformers import pipeline
from os import path, listdir, makedirs
from datetime import timedelta
from time import monotonic
from argparse import ArgumentParser

parser = ArgumentParser(prog='main.py')
parser.add_argument('-m', '--minimal', action='store_true')
args = parser.parse_args()

positive_categories = ['semantic', 'mistranslation', 'instruction', 'assembly'] # to add: register
negative_categories = ['other', 'boot', 'network', 'KVM', 'vnc', 'graphic', 'device', 'socket'] # to add: performance
categories = positive_categories + negative_categories

def list_files_recursive(directory):
    result = []
    for entry in listdir(directory):
        full_path = path.join(directory, entry)
        if path.isdir(full_path):
            result = result + list_files_recursive(full_path)
        else:
            result.append(full_path)
    return result

def output(text : str, category : str, labels : list, scores : list, identifier : str):
    file_path = f"output/{category}/{identifier}"
    makedirs(path.dirname(file_path), exist_ok = True)

    with open(file_path, "w") as file:
        for label, score in zip(labels, scores):
            file.write(f"{label}: {score:.3f}\n")

        file.write("\n")
        file.write(text)

def main():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    bugs = list_files_recursive("../results/scraper/mailinglist")
    if args.minimal:
        bugs = bugs + list_files_recursive("./semantic_issues")
    else:
        bugs = bugs + list_files_recursive("../results/scraper/launchpad")
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/issues_text")

    print(f"{len(bugs)} number of bugs will be processed")
    for bug in bugs:
        print(f"Processing {bug}")
        with open(bug, "r") as file:
            text = file.read()

        result = classifier(text, categories, multi_label=True)
        category = result['labels'][0]

        for label, score in zip(result["labels"], result["scores"]):
            if label in negative_categories and score >= 0.92:
                category = label
                break

        output(text, category, result['labels'], result['scores'], path.basename(bug))

if __name__ == "__main__":
    start_time = monotonic()
    main()
    end_time = monotonic()
    print(timedelta(seconds=end_time - start_time))
