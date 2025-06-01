from os import listdir, path

directory : str = "./test_input"

def test(classifier, categories):
    for name in listdir(directory):
        if name == "README.md":
            continue

        with open(path.join(directory, name), "r") as file:
            text = file.read()

        result = classifier(text, categories, multi_label=True)

        print(name)
        for label, score in zip(result["labels"], result["scores"]):
            print(f"{label}: {score:.3f}")
        print("")
