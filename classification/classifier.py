from transformers import pipeline
from os import path, listdir, makedirs
from datetime import timedelta
from time import monotonic
from argparse import ArgumentParser

parser = ArgumentParser(prog='classifier.py')
parser.add_argument('-f', '--full', action='store_true', help="use whole dataset")
parser.add_argument('-m', '--multi_label', action='store_true', help="enable multi_label for the classifier")
parser.add_argument('--model', default="facebook/bart-large-mnli", type=str, help="main model to use")
parser.add_argument('--compare', nargs='?', const="MoritzLaurer/deberta-v3-large-zeroshot-v2.0", type=str, help="second model for comparison")
args = parser.parse_args()

positive_categories = ['semantic', 'TCG', 'assembly', 'architecture', 'mistranslation', 'register', 'x86', 'arm', 'risc-v']
negative_categories = ['other', 'boot', 'network', 'kernel virtual machine', 'vnc', 'graphic', 'device', 'socket', 'debug', 'files', 'PID', 'permissions', 'performance']
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
            if label == "SPLIT":
                file.write(f"--------------------\n")
            else:
                file.write(f"{label}: {score:.3f}\n")

        file.write("\n")
        file.write(text)

def get_category(classification : dict):
    result = classification['labels'][0]

    if not args.multi_label:
        return result

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
    classifier = pipeline("zero-shot-classification", model=args.model)
    if args.compare:
        compare_classifier = pipeline("zero-shot-classification", model=args.compare)

    bugs = list_files_recursive("../results/scraper/mailinglist")
    if not args.full:
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/semantic_issues")
    else:
        bugs = bugs + list_files_recursive("../results/scraper/launchpad")
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/issues_text")

    print(f"{len(bugs)} number of bugs will be processed")
    for bug in bugs:
        print(f"Processing {bug}")
        with open(bug, "r") as file:
            text = file.read()

        result = classifier(text, categories, multi_label=args.multi_label)
        category = get_category(result)

        if args.compare:
            compare_result = compare_classifier(text, categories, multi_label=args.multi_label)
            compare_category = get_category(compare_result)

            if category != compare_category:
                category = "review"

            result['labels'] = result['labels'] + ['SPLIT'] + compare_result['labels']
            result['scores'] = result['scores'] + [0] + compare_result['scores']

        output(text, category, result['labels'], result['scores'], path.basename(bug))

if __name__ == "__main__":
    start_time = monotonic()
    main()
    end_time = monotonic()
    print(timedelta(seconds=end_time - start_time))
