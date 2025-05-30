from transformers import pipeline
from argparse import ArgumentParser

from test import test

parser = ArgumentParser(prog='classifier')
parser.add_argument('-d', '--deepseek', action='store_true')
args = parser.parse_args()

def main():
    if args.deepseek:
        print("deepseek not supported")
    else:
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        test(classifier)

if __name__ == "__main__":
    main()
