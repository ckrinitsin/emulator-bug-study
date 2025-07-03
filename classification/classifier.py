from transformers import pipeline
from os import path, listdir, makedirs
from datetime import timedelta
from time import monotonic
from argparse import ArgumentParser
from ollama import chat, ChatResponse
from re import sub

parser = ArgumentParser(prog='classifier.py')
parser.add_argument('-f', '--full', action='store_true', help="use whole dataset")
parser.add_argument('-m', '--multi_label', action='store_true', help="enable multi_label for the classifier")
parser.add_argument('-d', '--deepseek', nargs='?', const="deepseek-r1:7b", type=str, help="use deepseek")
parser.add_argument('--model', default="facebook/bart-large-mnli", type=str, help="main model to use")
parser.add_argument('--compare', nargs='?', const="MoritzLaurer/deberta-v3-large-zeroshot-v2.0", type=str, help="second model for comparison")
args = parser.parse_args()

positive_categories = ['semantic', 'TCG', 'assembly', 'architecture', 'mistranslation', 'register', 'user-level']
architectures = ['x86', 'arm', 'risc-v', 'i386', 'ppc']
negative_categories = ['boot', 'network', 'kvm', 'vnc', 'graphic', 'device', 'socket', 'debug', 'files', 'PID', 'permissions', 'performance', 'kernel', 'peripherals', 'VMM', 'hypervisor', 'virtual', 'other']
categories = positive_categories + negative_categories + architectures

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

def output(text : str, category : str, labels : list, scores : list, identifier : str, reasoning : str = None):
    print(f"Category: {category}, Time: {timedelta(seconds=monotonic() - start_time)}")
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

    if reasoning:
        file_path = f"reasoning/{category}/{identifier}"
        makedirs(path.dirname(file_path), exist_ok = True)

        with open(file_path, "w") as file:
            file.write(reasoning)

def get_category(classification : dict):
    highest_category = classification['labels'][0]

    if not args.multi_label:
        return highest_category 

    if all(i < 0.8 for i in classification["scores"]):
        return "none"
    elif sum(1 for i in classification["scores"] if i > 0.85) >= 20:
        return "all"
    elif classification["scores"][0] - classification["scores"][-1] <= 0.2:
        return "unknown"

    result = highest_category
    arch = None
    pos = None
    for label, score in zip(classification["labels"], classification["scores"]):
        if label in negative_categories and (not arch and not pos or score >= 0.92):
            return label

        if label in positive_categories and not pos and score > 0.8:
            pos = label
            if not arch:
                result = label
            else:
                result = label + "-" + arch

        if label in architectures and not arch and score > 0.8:
            arch = label
            if pos:
                result = pos + "-" + label

    return result

def compare_category(classification : dict, category : str):

    for label, score in zip(classification["labels"], classification["scores"]):
        if label in positive_categories and score >= 0.85:
            return category
        if label in category and score >= 0.85:
            return category

    return "review"

def main():
    if not args.deepseek:
        classifier = pipeline("zero-shot-classification", model=args.model)
        print(f"The model {args.model} will be used")
        if args.compare:
            compare_classifier = pipeline("zero-shot-classification", model=args.compare)
            print(f"The comparison model {args.compare} will be used")
    else:
        print(f"The model {args.deepseek} will be used")
        with open("preambel", "r") as file:
            preambel = file.read()

    processed_bugs = list_files_recursive("output", True)
    bugs = list_files_recursive("../results/scraper/mailinglist")
    bugs = []
    if not args.full:
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/semantic_issues")
        bugs = bugs + [ "../results/scraper/launchpad/1809546", "../results/scraper/launchpad/1156313" ]
    else:
        bugs = bugs + list_files_recursive("../results/scraper/launchpad-without-comments")
        bugs = bugs + list_files_recursive("../results/scraper/gitlab/issues_text")

    print(f"{len(bugs)} number of bugs will be processed")
    for i, bug in enumerate(bugs):
        print(f"Bug: {bug}, Number: {i+1},", end=" ")

        if path.basename(bug) in processed_bugs:
            print("skipped")
            continue

        with open(bug, "r") as file:
            text = file.read()

        if args.deepseek:
            response = chat(args.deepseek, [{'role': 'user', 'content': text + "\n" + preambel,}])
            category = sub(r'[^a-zA-Z]', '', response['message']['content'].split()[-1]).lower()
            if not category in categories:
                category = "manual-review"
            output(text, category, [], [], path.basename(bug), response['message']['content'])
        else:
            result = classifier(text, categories, multi_label=args.multi_label)
            category = get_category(result)

            if args.compare and sum(1 for i in positive_categories if i in category) >= 1:
                compare_result = compare_classifier(text, categories, multi_label=args.multi_label)
                category = compare_category(compare_result, category)

                result['labels'] = result['labels'] + ['SPLIT'] + compare_result['labels']
                result['scores'] = result['scores'] + [0] + compare_result['scores']

            output(text, category, result['labels'], result['scores'], path.basename(bug))

if __name__ == "__main__":
    start_time = monotonic()
    main()
    end_time = monotonic()
    print(timedelta(seconds=end_time - start_time))
