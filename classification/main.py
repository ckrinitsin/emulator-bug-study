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

categories = ['semantic', 'other', 'mistranslation', 'instruction']

def main():
    if args.deepseek:
        print("deepseek currently not supported")
        exit()

    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    if args.test:
        test(classifier, categories)
        exit()

    bugs = list_files_recursive("../mailinglist/output_mailinglist")
    for bug in bugs:
        with open(bug, "r") as file:
            text = file.read()

        result = classifier(text, categories, multi_label=True)
        output(text, result['labels'], result['scores'], path.basename(bug))

if __name__ == "__main__":
    main()
