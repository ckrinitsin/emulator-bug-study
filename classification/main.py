from transformers import pipeline
from argparse import ArgumentParser
from os import path

from test import test
from files import list_files_recursive
from output import output

parser = ArgumentParser(prog='classifier')
parser.add_argument('-d', '--deepseek', action='store_true')
parser.add_argument('-t', '--test', action='store_true')
args = parser.parse_args()

positive_categories = ['semantic', 'mistranslation', 'instruction', 'assembly'] # to add: register
negative_categories = ['other', 'boot', 'network', 'KVM', 'vnc', 'graphic', 'device', 'socket'] # to add: performance
categories = positive_categories + negative_categories

def main():
    if args.deepseek:
        print("deepseek currently not supported")
        exit()

    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    if args.test:
        test(classifier, categories)
        exit()

    bugs = list_files_recursive("../mailinglist/output_mailinglist")
    bugs = bugs + list_files_recursive("./semantic_issues")
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
    main()
