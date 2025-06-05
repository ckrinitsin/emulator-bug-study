from transformers import pipeline
from os import path, listdir, makedirs
from datetime import timedelta
from time import monotonic
from argparse import ArgumentParser

parser = ArgumentParser(prog='main.py')
parser.add_argument('-m', '--minimal', action='store_true')
args = parser.parse_args()

positive_categories = ['semantic']
negative_categories = ['other', 'boot', 'network', 'KVM', 'vnc', 'graphic', 'device', 'socket', 'debug', 'files', 'PID', 'permissions', 'performance']
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

def get_category(classification : dict):
    result = classification['labels'][0]

    for label, score in zip(classification["labels"], classification["scores"]):
        if label in negative_categories and score >= 0.92:
            result = label
            break

    if classification['labels'][0] == "semantic" and classification['scores'][0] <= 0.91:
        result = "other"

    if all(i > 0.9 for i in classification["scores"]):
        result = "all"
    elif all(i < 0.6 for i in classification["scores"]):
        result = "none"

    return result

def main():
    classifier_one = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    classifier_two = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    bugs = list_files_recursive("../results/scraper/mailinglist")
    if args.minimal:
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/semantic_issues")
    else:
        bugs = bugs + list_files_recursive("../results/scraper/launchpad")
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/issues_text")

    print(f"{len(bugs)} number of bugs will be processed")
    for bug in bugs:
        print(f"Processing {bug}")
        with open(bug, "r") as file:
            text = file.read()

        result_one = classifier_one(text, categories, multi_label=True)
        result_two = classifier_two(text, categories, multi_label=True)

        category_one = get_category(result_one)
        category_two = get_category(result_two)

        category = category_one
        if category_one != category_two:
            category = "review"

        output(text, category, result_one['labels']+result_two['labels'], result_one['scores']+result_two['scores'], path.basename(bug))

if __name__ == "__main__":
    start_time = monotonic()
    main()
    end_time = monotonic()
    print(timedelta(seconds=end_time - start_time))
